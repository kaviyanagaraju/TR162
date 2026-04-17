import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_income_trend(daily_df, lean_days_df=None, threshold=None):
    """
    Plots a line chart of income over time. Highlights lean periods.
    """
    fig = go.Figure()
    
    # Income Line
    fig.add_trace(go.Scatter(
        x=daily_df['Date'],
        y=daily_df['Income'],
        mode='lines+markers',
        name='Income',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))
    
    # Expense Line
    fig.add_trace(go.Scatter(
        x=daily_df['Date'],
        y=daily_df['Expense'],
        mode='lines+markers',
        name='Expense',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8)
    ))
    
    # Highlight Threshold
    if threshold:
        fig.add_hline(y=threshold, line_dash="dash", line_color="orange", 
                      annotation_text="Lean Threshold", annotation_position="bottom right")
                      
    # Highlight Lean Months markers
    if lean_days_df is not None and not lean_days_df.empty:
        fig.add_trace(go.Scatter(
            x=lean_days_df['Date'],
            y=lean_days_df['Income'],
            mode='markers',
            name='Lean Period',
            marker=dict(color='red', size=12, symbol='x')
        ))

    fig.update_layout(
        title="Income & Expense Trends",
        xaxis_title="Date",
        yaxis_title="Amount (₹)",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig

def plot_expense_distribution(df):
    """
    Plots a pie chart of expenses by category.
    """
    # Filter only expenses greater than 0
    expense_df = df[df['Expense'] > 0]
    
    if expense_df.empty:
        return None
        
    category_totals = expense_df.groupby('Category')['Expense'].sum().reset_index()
    
    fig = px.pie(
        category_totals, 
        values='Expense', 
        names='Category',
        title="Expense Distribution by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template="plotly_white")
    return fig
