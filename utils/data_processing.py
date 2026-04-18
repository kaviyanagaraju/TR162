import pandas as pd
import numpy as np
import io

def load_and_clean_data(file_or_df):
    """
    Super-Detective Reader: Handles BOM, different delimiters, and 2-digit years.
    """
    try:
        if isinstance(file_or_df, pd.DataFrame):
            df = file_or_df.copy()
        else:
            # Read and handle Byte Order Mark (BOM) from Excel
            raw_data = file_or_df.read()
            if isinstance(raw_data, bytes):
                content = raw_data.decode('utf-8-sig')
            else:
                content = raw_data
            
            # Try parsing with comma, fallback to semicolon
            try:
                df = pd.read_csv(io.StringIO(content), sep=',')
                if len(df.columns) < 2: raise Exception
            except:
                df = pd.read_csv(io.StringIO(content), sep=';')

        # Clean column names (Remove non-ASCII and strip)
        df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip().title() for col in df.columns]
        
        # Fuzzy find the Date column (handles " Date", "Date ", etc.)
        date_col = next((c for c in df.columns if 'Date' in c), None)
        if not date_col:
            return None, f"Error: Found columns {list(df.columns)}, but none named 'Date'."
        
        # Robust Date Parser
        def force_day_first(date_str):
            try:
                ds = str(date_str).strip().replace('/', '-')
                # Remove time portion if present
                ds_clean = ds.split(' ')[0]
                parts = ds_clean.split('-')
                
                if len(parts) == 3:
                     # Check if YYYY-MM-DD
                     if len(parts[0]) == 4:
                         return pd.Timestamp(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))
                     else:
                         # Handle DD-MM-YYYY or DD-MM-YY
                         d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                         if y < 100: y += 2000 # 26 -> 2026
                         return pd.Timestamp(year=y, month=m, day=d)
                return pd.to_datetime(ds_clean, dayfirst=True)
            except:
                return pd.NaT

        df['Date'] = df[date_col].apply(force_day_first)
        df = df.dropna(subset=['Date'])
        
        if df.empty:
            return None, "Error: All dates in this file are invalid. Ensure format is DD-MM-YYYY."

        # Numeric and other cleanups
        cmap = {'Working H': 'Working Hours', 'Work Hours': 'Working Hours', 'Cat': 'Category'}
        df = df.rename(columns=cmap)
        for col in ['Income', 'Expense', 'Tips', 'Working Hours']:
            df[col] = pd.to_numeric(df.get(col, 0), errors='coerce').fillna(0)

        return df.sort_values(by='Date').reset_index(drop=True), None
    except Exception as e:
        return None, f"Reader System Error: {str(e)}"
