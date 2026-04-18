import pandas as pd

def daily_aggregation(df):
    daily = df.groupby('Date').agg({
        'Income': 'sum', 'Tips': 'sum', 'Expense': 'sum', 'Working Hours': 'sum'
    }).reset_index()
    return daily

def monthly_aggregation(df):
    """
    Summarizes data by month for the snapshot table.
    """
    monthly = df.copy()
    monthly['Month'] = monthly['Date'].dt.strftime('%B %Y')
    summary = monthly.groupby(['Month']).agg({
        'Income': 'sum',
        'Tips': 'sum',
        'Expense': 'sum'
    }).reset_index()
    summary['Total Income'] = summary['Income'] + summary['Tips']
    summary['Net Savings'] = summary['Total Income'] - summary['Expense']
    return summary[['Month', 'Total Income', 'Expense', 'Net Savings']]

def predict_future_income(daily_df):
    if len(daily_df) < 2: return 0, 0
    avg_income = (daily_df['Income'] + daily_df['Tips']).mean()
    volatility = (daily_df['Income'] + daily_df['Tips']).std()
    return avg_income, volatility

def detect_lean_periods(daily_df):
    if daily_df.empty: return pd.DataFrame(), 0
    combined = daily_df['Income'] + daily_df['Tips']
    threshold = combined.mean() * 0.8
    lean_days = daily_df[combined < threshold]
    return lean_days, threshold
