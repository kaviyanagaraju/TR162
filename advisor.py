import random

def generate_recommendations(daily_df, prediction, volatility):
    """
    Generates high-intelligence, data-driven insights with embedded numerical facts.
    """
    recommendations = []
    
    if daily_df.empty:
        return ["👋 **Welcome!** Once you log your first shift, I will analyze your stats here."]

    # 1. Net Profitability Radar
    total_income = daily_df['Income'].sum()
    total_tips = daily_df['Tips'].sum()
    total_hours = daily_df['Working Hours'].sum()
    total_expense = daily_df['Expense'].sum()
    gross_total = total_income + total_tips
    
    if total_hours > 0:
        net_profit = gross_total - total_expense
        hourly_profit = net_profit / total_hours
        status = "🚀 **High Efficiency:**" if hourly_profit > 400 else "⚠️ **Low Efficiency:**"
        recommendations.append(
            f"{status} After expenses, you are taking home **₹{hourly_profit:,.2f} per hour**. "
            f"You've banked ₹{net_profit:,.2f} net profit over {total_hours:,.1f} total hours."
        )

    # 2. Expense Impact Intelligence
    if gross_total > 0:
        expense_ratio = (total_expense / gross_total) * 100
        if expense_ratio > 25:
            recommendations.append(
                f"🚩 **High Overhead:** Expenses are consuming **{expense_ratio:.1f}%** of your gross earnings. "
                "For gig workers, overhead above 20% usually indicates high fuel waste or maintenance issues."
            )
        else:
            recommendations.append(
                f"✅ **Lean Operation:** Excellent overhead control! Only **{expense_ratio:.1f}%** of your income went to expenses."
            )

    # 3. Weekly Burnout Radar
    recent_7_days_hours = daily_df['Working Hours'].tail(7).sum()
    if recent_7_days_hours > 55:
        recommendations.append(
            f"🚨 **Extreme Burnout Zone:** You have pushed **{recent_7_days_hours:.1f} hours** in the last 7 days. "
            "Exceeding 55 hours weekly leads to a 33% higher risk of health issues. Schedule a rest day immediately."
        )
    elif recent_7_days_hours > 40:
        recommendations.append(
            f"🕒 **Standard Full-Time:** You've clocked **{recent_7_days_hours:.1f} hours** this week. Fatigue management is recommended."
        )

    # 4. Volatility Protection
    safe_reserve = total_expense * 2.5 # 2.5 months of avg expenses as a safe buffer
    if volatility > (prediction * 0.3):
        recommendations.append(
            f"📊 **Income Volatility:** Your income swings by **₹{volatility:,.2f}** day-to-day. "
            f"To survive lean months, you should aim for a **₹{safe_reserve:,.2f}** emergency buffer."
        )
    
    # 5. Tax Compliance Fact
    tax_setaside = gross_total * 0.25
    recommendations.append(
        f"🏛️ **Tax Obligation:** Based on your earnings of ₹{gross_total:,.2f}, you should have **₹{tax_setaside:,.2f}** "
        "set aside for taxes today. Do not spend this amount!"
    )

    return recommendations

def ai_financial_response(query, daily_df_dict):
    """
    A rule-based chatbot replacement for financial advice based on simple NLP.
    """
    query = query.lower()
    
    if any(word in query for word in ['tax', 'taxes']):
        return "Based on standard independent contractor rules, it's generally advised to set aside 25-30% of your net income for taxes. Make sure you are tracking all deductible business expenses!"
    
    elif any(word in query for word in ['save', 'savings', 'emergency']):
        return "For gig workers, a 3-6 month emergency fund is crucial due to variable income. Look at your average monthly expenses and multiply by 3 to get your minimum goal."
        
    elif any(word in query for word in ['invest', 'investing', 'stocks']):
        return "Before investing heavily in stocks, ensure your high-interest debt is paid off and your emergency fund is fully funded. Once ready, look into low-cost index funds or a Solo 401(k) / SEP IRA if self-employed."
        
    elif any(word in query for word in ['budget', 'spending', 'expense']):
        tot_inc = daily_df['Income'].sum() if not daily_df.empty else 0
        return f"Based on your total historical income of ₹{tot_inc:,.2f}, applying the strict 50/30/20 budget means you should allocate: ₹{tot_inc*0.5:,.2f} for Needs (50%), ₹{tot_inc*0.3:,.2f} for Wants (30%), and ₹{tot_inc*0.2:,.2f} for Savings/Debt (20%)."
        
    elif any(word in query for word in ['overwork', 'hours', 'long', 'tired', 'burnout']):
        return "As a gig worker, it's easy to fall into the trap of overworking. For safety and health, try to limit gig shifts to 10-12 hours per day and plan at least one dedicated day off per week."
        
    elif any(word in query for word in ['water', 'drink', 'hydrate', 'thirst']):
        return "Staying hydrated directly impacts your focus and energy on the road! Keep a large reusable water bottle with you and aim to drink a little every hour. Set a timer if you need to!"
        
    elif any(word in query for word in ['food', 'lunch', 'dinner', 'break', 'meal', 'hungry']):
        return "Don't work completely straight through meals! For peak efficiency and wellbeing, take a dedicated 30-minute food/rest break every 4-6 hours. It pays off in better energy for the remainder of your shift."
    
    else:
        responses = [
            "That's a great question! While I am a simple AI, I'd recommend looking at your expense breakdown to find areas to optimize.",
            "As a gig worker, consistency is key. Always prioritize building a buffer for lean months.",
            "I can't answer that perfectly, but tracking your income vs expenses clearly is the first step to financial freedom!"
        ]
        return random.choice(responses)
