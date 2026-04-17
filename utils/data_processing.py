import pandas as pd
import numpy as pd_np
import numpy as np

def load_and_clean_data(file_or_df):
    """
    Loads a CSV file or DataFrame and cleans it.
    Expected columns: Date, Income, Expense, Description
    """
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            df = pd.read_csv(file_or_df)
        
        # Standardize column headers to title case and strip whitespace
        df.columns = [col.strip().title() for col in df.columns]
        
        req_columns = ['Date', 'Income', 'Expense', 'Description']
        
        missing_cols = [col for col in req_columns if col not in df.columns]
        if missing_cols:
            return None, f"Missing required columns: {', '.join(missing_cols)}"
            
        # Convert Date using DayFirst format for DD-MM-YYYY
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        
        # Handing missing values: Income and Expense defaults to 0
        df['Income'] = df['Income'].fillna(0).astype(float)
        df['Expense'] = df['Expense'].fillna(0).astype(float)
        
        if 'Tips' not in df.columns:
            df['Tips'] = 0.0
        df['Tips'] = df['Tips'].fillna(0).astype(float)
        
        if 'Working Hours' not in df.columns:
            df['Working Hours'] = 0.0
        df['Working Hours'] = df['Working Hours'].fillna(0).astype(float)
        
        # Drop rows where Date is NaT
        df = df.dropna(subset=['Date'])
        
        # Fill missing descriptions
        df['Description'] = df['Description'].fillna("Unknown")
        
        # Sort by date
        df = df.sort_values(by='Date').reset_index(drop=True)
        
        return df, None
    except Exception as e:
        return None, f"Error processing file: {e}"
