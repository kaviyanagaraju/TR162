import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_income_trend(daily_df, lean_days, threshold):
    """
    Plots daily income and savings trends with lean period highlighting.
    """
    if daily_df.empty:
        return None
    
    # Calculate daily savings
    daily_df['Savings'] = (daily_df['Income'] + daily_df['Tips']) - daily_df['Expense']
        
    fig = go.Figure()
    
    # Income Line
    fig.add_trace(go.Scatter(
        x=daily_df['Date'], y=daily_df['Income'] + daily_df['Tips'],
        mode='lines+markers', name='Total Income',
        line=dict(color='#2ecc71', width=3),
        hovertemplate='Date: %{x}<br>Income: ₹%{y:,.2f}'
    ))
    
    # Savings Line
    fig.add_trace(go.Scatter(
        x=daily_df['Date'], y=daily_df['Savings'],
        mode='lines+markers', name='Net Savings',
        line=dict(color='#3498db', width=3, dash='dot'),
        hovertemplate='Date: %{x}<br>Savings: ₹%{y:,.2f}'
    ))
    
    # Threshold Line
    fig.add_trace(go.Scatter(
        x=daily_df['Date'], y=[threshold]*len(daily_df),
        mode='lines', name='Lean Threshold',
        line=dict(color='#e74c3c', width=1, dash='dash'),
        hoverinfo='skip'
    ))
    
    # Highlight Lean Periods
    if lean_days is not None and not lean_days.empty:
        fig.add_trace(go.Scatter(
            x=lean_days['Date'], y=lean_days['Income'] + lean_days['Tips'],
            mode='markers', name='Lean Period',
            marker=dict(color='#e74c3c', size=12, symbol='x'),
            hovertemplate='LEAN PERIOD ALERT<br>Date: %{x}'
        ))

    fig.update_layout(
        title="Income & Savings Trends",
        xaxis_title="Date",
        yaxis_title="Amount (₹)",
        template="plotly_white",
        hovermode="x unified"
    )
    
    return fig

def plot_expense_distribution(df):
    """
    Creates a colorful pie chart of expenses by category.
    """
    if df.empty or df['Expense'].sum() == 0:
        return None
    
    # Group by category to ensure clean labels
    cat_df = df.groupby('Category')['Expense'].sum().reset_index()
    
    fig = px.pie(
        cat_df, 
        values='Expense', 
        names='Category', 
        hole=0.4,
        title='Expense Breakdown by Category',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=True, margin=dict(t=50, b=10, l=10, r=10))
    
    return fig
