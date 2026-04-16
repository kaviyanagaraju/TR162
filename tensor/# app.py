# app.py - AI Personal Finance Coach for Gig Workers

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Finance Coach - Gig Workers",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .insight-box {
        background-color: #f0f7ff;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def categorize_expense(description):
    """Automatically categorize expenses based on description keywords."""
    description = str(description).lower()
    
    food_keywords = ['food', 'restaurant', 'grocery', 'meal', 'lunch', 'dinner', 
                     'breakfast', 'coffee', 'cafe', 'pizza', 'burger', 'snack',
                     'uber eats', 'doordash', 'grubhub', 'swiggy', 'zomato']
    
    rent_keywords = ['rent', 'lease', 'housing', 'apartment', 'mortgage', 
                     'accommodation', 'landlord', 'property']
    
    travel_keywords = ['travel', 'uber', 'lyft', 'taxi', 'gas', 'fuel', 'petrol',
                       'metro', 'bus', 'train', 'flight', 'airline', 'parking',
                       'toll', 'car', 'vehicle', 'maintenance']
    
    bills_keywords = ['bill', 'electric', 'electricity', 'water', 'internet',
                      'phone', 'mobile', 'subscription', 'netflix', 'spotify',
                      'insurance', 'utility', 'gas bill', 'wifi']
    
    if any(keyword in description for keyword in food_keywords):
        return 'Food'
    elif any(keyword in description for keyword in rent_keywords):
        return 'Rent'
    elif any(keyword in description for keyword in travel_keywords):
        return 'Travel'
    elif any(keyword in description for keyword in bills_keywords):
        return 'Bills'
    else:
        return 'Others'


def calculate_moving_average(data, window=3):
    """Calculate simple moving average for income prediction."""
    if len(data) >= window:
        return data[-window:].mean()
    return data.mean()


def identify_lean_periods(monthly_income, threshold_percentile=25):
    """Identify months with income below the threshold percentile."""
    threshold = np.percentile(monthly_income['Income'], threshold_percentile)
    lean_months = monthly_income[monthly_income['Income'] < threshold]
    return lean_months, threshold


def create_savings_plan(total_income, total_expenses, savings_rate=0.20):
    """Create a savings plan with at least 20% of income."""
    recommended_savings = total_income * savings_rate
    actual_savings = total_income - total_expenses
    
    return {
        'recommended_savings': recommended_savings,
        'actual_savings': actual_savings,
        'savings_rate': savings_rate,
        'is_meeting_goal': actual_savings >= recommended_savings
    }


def estimate_tax(total_income, tax_rate=0.10):
    """Estimate tax as 10% of income."""
    return total_income * tax_rate


def create_sample_data():
    """Create sample CSV data for demonstration."""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    data = []
    
    np.random.seed(42)
    
    for date in dates:
        # Random income entries (gig worker pattern - irregular)
        if np.random.random() > 0.7:
            income = np.random.choice([50, 75, 100, 150, 200, 250, 300])
            descriptions = ['Uber ride', 'DoorDash delivery', 'Freelance work', 
                           'Task Rabbit job', 'Fiverr project', 'Instacart delivery']
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Income': income,
                'Expense': 0,
                'Description': np.random.choice(descriptions)
            })
        
        # Random expense entries
        if np.random.random() > 0.5:
            expense_types = [
                ('Grocery shopping', 30, 80, 'Food'),
                ('Restaurant dinner', 15, 50, 'Food'),
                ('Uber ride', 10, 30, 'Travel'),
                ('Gas station', 25, 60, 'Travel'),
                ('Monthly rent', 800, 1200, 'Rent'),
                ('Electric bill', 50, 150, 'Bills'),
                ('Phone bill', 40, 80, 'Bills'),
                ('Netflix subscription', 15, 20, 'Bills'),
                ('Online shopping', 20, 100, 'Others'),
            ]
            
            exp_type = expense_types[np.random.randint(0, len(expense_types))]
            
            # Make rent monthly
            if 'rent' in exp_type[0].lower() and date.day != 1:
                continue
                
            expense = np.random.randint(exp_type[1], exp_type[2])
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Income': 0,
                'Expense': expense,
                'Description': exp_type[0]
            })
    
    return pd.DataFrame(data)


# Main App
def main():
    st.markdown('<h1 class="main-header">💰 AI Personal Finance Coach</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Smart financial insights for gig workers</p>', 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("[img.icons8.com](https://img.icons8.com/clouds/200/money-bag.png)", width=150)
        st.markdown("### 📊 Data Upload")
        
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=['csv'],
            help="CSV should have columns: Date, Income, Expense, Description"
        )
        
        st.markdown("---")
        
        if st.button("📥 Use Sample Data", use_container_width=True):
            st.session_state['use_sample'] = True
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        savings_goal = st.slider(
            "Savings Goal (%)", 
            min_value=10, 
            max_value=50, 
            value=20,
            help="Set your target savings percentage"
        )
        
        tax_rate = st.slider(
            "Tax Rate (%)", 
            min_value=5, 
            max_value=30, 
            value=10,
            help="Estimated tax rate on income"
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📋 CSV Format
        ```
        Date,Income,Expense,Description
        2024-01-15,150,0,Uber ride
        2024-01-16,0,45,Grocery shopping
        ```
        """)
    
    # Load data
    df = None
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
    elif st.session_state.get('use_sample', False):
        df = create_sample_data()
        st.info("📊 Using sample data for demonstration")
    
    if df is not None:
        # Data preprocessing
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')
        df['Month_Name'] = df['Date'].dt.strftime('%b %Y')
        df['Category'] = df['Description'].apply(categorize_expense)
        
        # Calculate totals
        total_income = df['Income'].sum()
        total_expenses = df['Expense'].sum()
        net_balance = total_income - total_expenses
        
        # Tax estimation
        estimated_tax = estimate_tax(total_income, tax_rate/100)
        after_tax_income = total_income - estimated_tax
        
        # Savings plan
        savings_plan = create_savings_plan(total_income, total_expenses, savings_goal/100)
        
        # Monthly aggregation
        monthly_data = df.groupby('Month').agg({
            'Income': 'sum',
            'Expense': 'sum',
            'Date': 'first'
        }).reset_index()
        monthly_data['Month_Str'] = monthly_data['Month'].astype(str)
        
        # Identify lean periods
        lean_periods, lean_threshold = identify_lean_periods(monthly_data)
        
        # Predict next month's income
        predicted_income = calculate_moving_average(monthly_data['Income'], window=3)
        
        # Dashboard Layout
        st.markdown("## 📈 Financial Overview")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💵 Total Income",
                value=f"${total_income:,.2f}",
                delta=f"${predicted_income:,.0f} predicted next month"
            )
        
        with col2:
            st.metric(
                label="💸 Total Expenses",
                value=f"${total_expenses:,.2f}",
                delta=f"-{(total_expenses/total_income*100):.1f}% of income" if total_income > 0 else "N/A",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                label="💰 Net Balance",
                value=f"${net_balance:,.2f}",
                delta="Positive" if net_balance > 0 else "Negative",
                delta_color="normal" if net_balance > 0 else "inverse"
            )
        
        with col4:
            st.metric(
                label="🏛️ Estimated Tax (10%)",
                value=f"${estimated_tax:,.2f}",
                delta=f"After-tax: ${after_tax_income:,.2f}"
            )
        
        st.markdown("---")
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Monthly Income Trend")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            months = monthly_data['Month_Str'].tolist()
            incomes = monthly_data['Income'].tolist()
            
            # Plot income trend
            ax.plot(months, incomes, marker='o', linewidth=2.5, 
                   color='#1E88E5', markersize=8, label='Actual Income')
            
            # Add moving average line
            if len(incomes) >= 3:
                ma = pd.Series(incomes).rolling(window=3).mean()
                ax.plot(months, ma, '--', linewidth=2, 
                       color='#FFA726', label='3-Month Moving Avg')
            
            # Highlight lean periods
            for idx, row in lean_periods.iterrows():
                month_idx = months.index(row['Month_Str'])
                ax.axvspan(month_idx - 0.3, month_idx + 0.3, 
                          alpha=0.3, color='red', label='Lean Period' if idx == lean_periods.index[0] else "")
            
            # Add prediction point
            ax.scatter([len(months)], [predicted_income], 
                      color='#4CAF50', s=100, zorder=5, marker='*')
            ax.annotate(f'Predicted\n${predicted_income:,.0f}', 
                       xy=(len(months), predicted_income),
                       xytext=(len(months)-0.5, predicted_income + 200),
                       fontsize=9, color='#4CAF50')
            
            ax.set_xlabel('Month', fontsize=11)
            ax.set_ylabel('Income ($)', fontsize=11)
            ax.set_title('Income Over Time', fontsize=13, fontweight='bold')
            ax.legend(loc='upper left')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("### 🥧 Expense Breakdown by Category")
            
            expense_by_category = df[df['Expense'] > 0].groupby('Category')['Expense'].sum()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            explode = [0.05] * len(expense_by_category)
            
            wedges, texts, autotexts = ax.pie(
                expense_by_category.values,
                labels=expense_by_category.index,
                autopct='%1.1f%%',
                colors=colors[:len(expense_by_category)],
                explode=explode,
                shadow=True,
                startangle=90
            )
            
            for autotext in autotexts:
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')
            
            ax.set_title('Where Your Money Goes', fontsize=13, fontweight='bold')
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
        
        st.markdown("---")
        
        # Detailed Expense Table
        st.markdown("### 📋 Expense Categories Detail")
        
        expense_detail = df[df['Expense'] > 0].groupby('Category').agg({
            'Expense': ['sum', 'mean', 'count']
        }).round(2)
        expense_detail.columns = ['Total ($)', 'Average ($)', 'Transactions']
        expense_detail = expense_detail.sort_values('Total ($)', ascending=False)
        expense_detail['% of Total'] = (expense_detail['Total ($)'] / total_expenses * 100).round(1)
        
        st.dataframe(
            expense_detail.style.format({
                'Total ($)': '${:,.2f}',
                'Average ($)': '${:,.2f}',
                '% of Total': '{:.1f}%'
            }).background_gradient(cmap='Blues', subset=['Total ($)']),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # AI Insights Section
        st.markdown("## 🤖 AI Financial Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Income Prediction
            st.markdown("### 🔮 Income Prediction")
            st.markdown(f"""
            <div class="insight-box">
                <h4>Next Month's Predicted Income</h4>
                <p style="font-size: 2rem; font-weight: bold; color: #1E88E5;">${predicted_income:,.2f}</p>
                <p>Based on 3-month simple moving average of your earnings.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Lean Periods Warning
            if len(lean_periods) > 0:
                st.markdown("### ⚠️ Lean Periods Identified")
                lean_months_str = ', '.join(lean_periods['Month_Str'].tolist())
                st.markdown(f"""
                <div class="warning-box">
                    <h4>Low Income Months</h4>
                    <p><strong>{lean_months_str}</strong></p>
                    <p>These months had income below ${lean_threshold:,.2f} (25th percentile).</p>
                    <p><em>Tip: Build an emergency fund to cover 3-6 months of expenses.</em></p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Savings Plan
            st.markdown("### 💎 Savings Plan")
            
            if savings_plan['is_meeting_goal']:
                st.markdown(f"""
                <div class="success-box">
                    <h4>✅ Great Job! You're Meeting Your Savings Goal</h4>
                    <p><strong>Target ({savings_goal}%):</strong> ${savings_plan['recommended_savings']:,.2f}</p>
                    <p><strong>Actual Savings:</strong> ${savings_plan['actual_savings']:,.2f}</p>
                    <p>You're saving {(savings_plan['actual_savings']/total_income*100):.1f}% of your income!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                shortfall = savings_plan['recommended_savings'] - savings_plan['actual_savings']
                st.markdown(f"""
                <div class="warning-box">
                    <h4>📉 Savings Goal Not Met</h4>
                    <p><strong>Target ({savings_goal}%):</strong> ${savings_plan['recommended_savings']:,.2f}</p>
                    <p><strong>Actual Savings:</strong> ${savings_plan['actual_savings']:,.2f}</p>
                    <p><strong>Shortfall:</strong> ${shortfall:,.2f}</p>
                    <p><em>Consider reducing expenses in 'Others' or 'Food' categories.</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Tax Summary
            st.markdown("### 🏛️ Tax Estimation")
            st.markdown(f"""
            <div class="insight-box">
                <h4>Estimated Tax Liability ({tax_rate}%)</h4>
                <p style="font-size: 1.5rem; font-weight: bold; color: #E53935;">${estimated_tax:,.2f}</p>
                <p><strong>After-Tax Income:</strong> ${after_tax_income:,.2f}</p>
                <p><em>Set aside ${estimated_tax/12:,.2f}/month for taxes.</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Actionable Recommendations
        st.markdown("## 💡 Personalized Recommendations")
        
        recommendations = []
        
        # Check highest expense category
        if 'Food' in expense_by_category.index:
            food_pct = expense_by_category['Food'] / total_expenses * 100
            if food_pct > 30:
                recommendations.append(f"🍔 **Food expenses are {food_pct:.1f}% of total.** Consider meal prepping to reduce costs.")
        
        # Check if rent is too high
        if 'Rent' in expense_by_category.index:
            rent_pct = expense_by_category['Rent'] / total_income * 100
            if rent_pct > 30:
                recommendations.append(f"🏠 **Rent is {rent_pct:.1f}% of income.** Ideally, keep housing under 30%.")
        
        # Check savings rate
        if not savings_plan['is_meeting_goal']:
            recommendations.append(f"💰 **Increase savings by ${savings_plan['recommended_savings'] - savings_plan['actual_savings']:,.2f}** to meet your {savings_goal}% goal.")
        
        # Emergency fund recommendation
        monthly_expense_avg = total_expenses / len(monthly_data)
        emergency_fund_target = monthly_expense_avg * 6
        recommendations.append(f"🛡️ **Build an emergency fund of ${emergency_fund_target:,.2f}** (6 months of expenses).")
        
        # Tax preparation
        recommendations.append(f"📅 **Set aside ${estimated_tax/12:,.2f} monthly** for quarterly tax payments.")
        
        # Income diversification for gig workers
        recommendations.append("📱 **Diversify income streams** - Consider adding 1-2 more gig platforms to stabilize earnings.")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown("---")
        
        # Data Preview
        with st.expander("📊 View Raw Data"):
            st.dataframe(df.sort_values('Date', ascending=False).head(50))
        
        # Download processed data
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Processed Data",
            data=csv_buffer.getvalue(),
            file_name="processed_finance_data.csv",
            mime="text/csv"
        )
    
    else:
        # Welcome screen when no data is loaded
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h2>Welcome to AI Personal Finance Coach! 👋</h2>
            <p style="font-size: 1.2rem; color: #666;">
                Upload your financial data or use sample data to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f5f5f5; border-radius: 15px;">
                <h3>📤 Upload Data</h3>
                <p>Upload your CSV file with income and expense data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f5f5f5; border-radius: 15px;">
                <h3>🤖 AI Analysis</h3>
                <p>Get automatic categorization and smart insights</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f5f5f5; border-radius: 15px;">
                <h3>💡 Take Action</h3>
                <p>Receive personalized recommendations</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    if 'use_sample' not in st.session_state:
        st.session_state['use_sample'] = False
    main() 