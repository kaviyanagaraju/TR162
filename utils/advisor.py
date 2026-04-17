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

def ai_financial_response(query, daily_df):
    """
    Advanced data-driven chatbot that uses real session stats to answer questions.
    """
    query = query.lower()
    
    # Calculate key stats for the response
    tot_inc = daily_df['Income'].sum() if not daily_df.empty else 0
    tot_exp = daily_df['Expense'].sum() if not daily_df.empty else 0
    net_sav = tot_inc - tot_exp
    avg_monthly_exp = daily_df['Expense'].mean() * 30 if not daily_df.empty else 0
    
    if any(word in query for word in ['tax', 'taxes']):
        tax_est = tot_inc * 0.25
        return f"Based on your gross income of ₹{tot_inc:,.2f}, you should reserve ₹{tax_est:,.2f} (25%) for taxes. You currently have ₹{net_sav:,.2f} in net savings."
    
    elif any(word in query for word in ['loan', 'borrow', 'debt', 'emi']):
        if daily_df.empty:
            return "I need some data to analyze your loan eligibility. Please enter your finances first!"
        
        # Risk Analysis
        months_buffer = net_sav / avg_monthly_exp if avg_monthly_exp > 0 else 0
        
        analysis = ""
        if months_buffer > 3:
            analysis = (f"📊 **Data-Driven Analysis:** Your ₹{net_sav:,.2f} savings cover **{months_buffer:.1f} months** of expenses. This is a very strong 'Safety Shield'.\n\n")
        else:
            analysis = (f"⚠️ **Warning:** Your savings (₹{net_sav:,.2f}) only cover **{months_buffer:.1f} months**. Taking a loan now is high-risk.\n\n")

        tips = (
            "✅ **Pros:** Can help with big necessary purchases (like a new bike) or consolidate high-interest debt.\n"
            "❌ **Cons:** EMI is a fixed cost while gig income is variable; one bad week can lead to a missed payment.\n\n"
            "💡 **Expert Tips for You:**\n"
            "1. **The 15% Rule:** Never let your total monthly EMIs exceed 15% of your average monthly gig income.\n"
            "2. **Interest Check:** Avoid 'Instant App' loans; their high interest rates (36%+) can trap gig workers in a debt cycle.\n"
            "3. **Rainy Day:** Always keep at least 1 month's EMI amount extra in your account at all times."
        )
        return analysis + tips

    elif any(word in query for word in ['save', 'savings', 'emergency']):
        target = avg_monthly_exp * 3
        deficit = target - net_sav
        if deficit > 0:
            return f"Your current savings are ₹{net_sav:,.2f}. To be safe, you need a 3-month fund of ₹{target:,.2f}. You are ₹{deficit:,.2f} away from your safety goal."
        return f"Amazing! Your ₹{net_sav:,.2f} savings have already exceeded your 3-month safety target of ₹{target:,.2f}. You are financially secure!"
        
    elif any(word in query for word in ['invest', 'stocks', 'mutual']):
        if net_sav < (avg_monthly_exp * 2):
            return "I don't recommend investing in stocks yet. You first need a larger emergency buffer. Keep saving until you have at least 2 months of expenses safe."
        return "You have a solid buffer! You could consider low-risk investments with any surplus above your emergency fund."

    elif any(word in query for word in ['overwork', 'burnout', 'hours']):
        tot_hrs = daily_df['Working Hours'].sum()
        return f"You've logged {tot_hrs:.1f} total hours. If this averages to more than 50 hours a week, I recommend a 48-hour total disconnect to refresh your focus."

    else:
        return "I can help with specific questions about your **Taxes**, **Loan Eligibility**, **Savings Goals**, or **Burnout**. Try asking: 'Can I afford a loan?'"
