import pandas as pd
import numpy as np

def load_and_clean_data(file_or_df):
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            df = pd.read_csv(file_or_df)
        
        df.columns = [col.strip().title() for col in df.columns]
        
        # Manual Date Splitter (Bulletproof Fix)
        def force_day_first(date_str):
            try:
                date_str = str(date_str).replace('/', '-')
                parts = date_str.split('-')
                if len(parts) == 3:
                     # Force: Day-Month-Year (e.g. 06-04-2026)
                     return pd.Timestamp(year=int(parts[2]), month=int(parts[1]), day=int(parts[0]))
                return pd.to_datetime(date_str, dayfirst=True)
            except:
                return pd.NaT

        df['Date'] = df['Date'].apply(force_day_first)
        
        # Standardize Numbers
        col_map = {'Working H': 'Working Hours', 'Work Hours': 'Working Hours', 'Cat': 'Category'}
        df = df.rename(columns=col_map)
        
        for col in ['Income', 'Expense', 'Tips', 'Working Hours']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0.0
        
        df = df.dropna(subset=['Date'])
        return df, None
    except Exception as e:
        return None, f"Error: {e}"

        
        
