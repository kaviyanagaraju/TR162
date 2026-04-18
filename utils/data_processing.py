import pandas as pd
import numpy as np

def load_and_clean_data(file_or_df):
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            df = pd.read_csv(file_or_df)
        
        # Standardize headers
        df.columns = [col.strip().title() for col in df.columns]
        
        # Fuzzy Rename
        col_map = {'Working H': 'Working Hours', 'Work Hours': 'Working Hours', 'Cat': 'Category'}
        df = df.rename(columns=col_map)

        # Smart Multi-Format Parser
        def smart_date(col):
            # Try 1: Strict DD-MM-YYYY (April Fix)
            res = pd.to_datetime(col, format='%d-%m-%Y', errors='coerce')
            # Try 2: Strict DD/MM/YYYY
            if res.isna().sum() > len(res) * 0.5:
                res = pd.to_datetime(col, format='%d/%m/%Y', errors='coerce')
            # Try 3: General DayFirst
            if res.isna().sum() > len(res) * 0.5:
                res = pd.to_datetime(col, dayfirst=True, errors='coerce')
            return res

        df['Date'] = smart_date(df['Date'])
        
        # Drop rows with no dates
        df = df.dropna(subset=['Date'])
        
        if df.empty:
            return None, "Error: No valid dates found in file. Please ensure dates are like 06-04-2026."

        # Convert numbers strictly
        for col in ['Income', 'Expense', 'Tips', 'Working Hours']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0.0
        
        df['Description'] = df.get('Description', pd.Series(['Activity']*len(df))).fillna("Unknown")
        df['Category'] = df.get('Category', pd.Series(['Others']*len(df))).fillna("Others")
        
        return df.sort_values('Date').reset_index(drop=True), None
    except Exception as e:
        return None, f"System Error: {e}"

        
        
