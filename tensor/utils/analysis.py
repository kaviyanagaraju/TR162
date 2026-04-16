import pandas as pd
import numpy as np

def daily_aggregation(df):
    """
    Aggregates data by day.
    """
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date']).dt.date
    
    if 'Working Hours' not in df_copy.columns:
        df_copy['Working Hours'] = 0.0
        
    daily_summary = df_copy.groupby('Date').agg({
        'Income': 'sum',
        'Tips': 'sum',
        'Working Hours': 'sum',
        'Expense': 'sum'
    }).reset_index()
    
    # Bundle tips into total daily income for modeling and graphing
    daily_summary['Income'] = daily_summary['Income'] + daily_summary['Tips']
    
    daily_summary['Date'] = daily_summary['Date'].astype(str)
    daily_summary['Net_Savings'] = daily_summary['Income'] - daily_summary['Expense']
    
    return daily_summary

def predict_future_income(daily_df, window=7):
    """
    Predicts next day's income using a Simple Moving Average (SMA) 
    over the given window of days.
    """
    if len(daily_df) < 1:
        return 0, 0
    
    if len(daily_df) < window:
        window = len(daily_df)
        
    recent_income = daily_df['Income'].tail(window)
    prediction = recent_income.mean()
    volatility = recent_income.std() if len(recent_income) > 1 else 0
    
    return prediction, volatility

def detect_lean_periods(daily_df, threshold_ratio=0.8):
    """
    Identifies days where income drops below a threshold (e.g., 80% of mean).
    """
    if len(daily_df) == 0:
        return pd.DataFrame(), None
        
    mean_income = daily_df['Income'].mean()
    threshold = mean_income * threshold_ratio
    
    lean_days = daily_df[daily_df['Income'] < threshold].copy()
    return lean_days, threshold
