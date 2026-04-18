import pandas as pd
import numpy as np

def load_and_clean_data(file_or_df):
    """
    Loads a CSV file or DataFrame and cleans it.
    Features: Strict DD-MM-YYYY parsing and fuzzy column matching.
    """
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            df = pd.read_csv(file_or_df)
        
        # Standardize column headers to title case and strip whitespace
        df.columns = [col.strip().title() for col in df.columns]
        
        # Smart column renaming for Excel-style headers
        col_map = {
            'Working H': 'Working Hours',
            'Work Hours': 'Working Hours',
            'Cat': 'Category'
        }
        df = df.rename(columns=col_map)
        
        # Multi-stage date parser for maximum compatibility (Forces April over June)
        def parse_dates(col):
            # Try strict DD-MM-YYYY first
            res = pd.to_datetime(col, format='%d-%m-%Y', errors='coerce')
            # If failed, try DD/MM/YYYY
            if res.isna().all():
                res = pd.to_datetime(col, format='%d/%m/%Y', errors='coerce')
            # Final fallback
            if res.isna().all():
                res = pd.to_datetime(col, dayfirst=True, errors='coerce')
            return res

        df['Date'] = parse_dates(df['Date'])
        
        # Standardize Numbers
        for col in ['Income', 'Expense', 'Tips', 'Working Hours']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0.0
        
        # Safety: Drop rows without dates
        df = df.dropna(subset=['Date'])
        
        # Fill missing text
        if 'Description' not in df.columns: df['Description'] = 'Activity'
        df['Description'] = df['Description'].fillna("Unknown")
        
        if 'Category' not in df.columns: df['Category'] = 'Others'
        df['Category'] = df['Category'].fillna("Others")
        
        # Sort by date
        df = df.sort_values(by='Date').reset_index(drop=True)
        
        return df, None
    except Exception as e:
        return None, f"Error processing: {e}"
