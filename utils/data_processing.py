import pandas as pd
import numpy as np

def load_and_clean_data(file_or_df):
    """
    Bulletproof CSV reader that forces Day-Month-Year parsing.
    """
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            df = pd.read_csv(file_or_df)
        
        # Consistent headers
        df.columns = [col.strip().title() for col in df.columns]
        
        # Manual Date Parser (Fixes the April/June swap)
        def force_day_first(date_str):
            try:
                ds = str(date_str).replace('/', '-')
                parts = ds.split('-')
                if len(parts) == 3:
                     # Force Day-Month-Year
                     return pd.Timestamp(year=int(parts[2]), month=int(parts[1]), day=int(parts[0]))
                return pd.to_datetime(ds, dayfirst=True)
            except:
                return pd.NaT

        df['Date'] = df['Date'].apply(force_day_first)
        df = df.dropna(subset=['Date'])
        
        # Smarter column mapping
        cmap = {'Working H': 'Working Hours', 'Work Hours': 'Working Hours', 'Cat': 'Category'}
        df = df.rename(columns=cmap)

        # Standardize numeric columns
        for col in ['Income', 'Expense', 'Tips', 'Working Hours']:
            df[col] = pd.to_numeric(df.get(col, 0), errors='coerce').fillna(0)

        # Sort and return
        return df.sort_values(by='Date').reset_index(drop=True), None
    except Exception as e:
        return None, f"System Error: {e}"
