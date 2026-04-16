import random

def generate_recommendations(daily_df, prediction, volatility):
    """
    Generates rule-based recommendations for gig workers based on their data.
    """
    recommendations = []
    
    avg_expense = daily_df['Expense'].mean() if not daily_df.empty else 0
    
    # Adaptive savings plan
    savings_rate = 0.2
    if volatility > 0.3:
        savings_rate = 0.3
        recommendations.append(
            f"📊 **High Volatility Detected:** Your income fluctuates by {volatility*100:.0f}%. We recommend increasing your savings target to {savings_rate*100:.0f}% to build a stronger emergency fund."
        )
    else:
        recommendations.append(
            f"💡 **Consistent Income:** Your income is relatively stable. Aim to save at least {savings_rate*100:.0f}% of your predicted income (₹{prediction * savings_rate:,.2f}) for future security."
        )
        
    # Savings Deficit vs Surplus logic
    total_income = daily_df['Income'].sum() if not daily_df.empty else 0
    total_expense = daily_df['Expense'].sum() if not daily_df.empty else 0
    actual_savings = total_income - total_expense
    target_savings = total_income * savings_rate
    
    if total_income > 0:
        if actual_savings < target_savings:
            recommendations.append(f"📉 **Savings Deficit:** You've banked **₹{actual_savings:,.2f}** so far. But based on your {savings_rate*100:.0f}% safe goal against your historical income, you should actually have **₹{target_savings:,.2f}** saved. Look closely at your expense categories and cut back!")
        else:
            recommendations.append(f"🎉 **Savings Goal Met:** Fantastic! You've banked **₹{actual_savings:,.2f}** in pure savings, which safely tracks above your minimum strong target of ₹{target_savings:,.2f}.")
        
    if avg_expense > prediction:
        recommendations.append(
            "🚨 **Overspending Risk:** Your average daily expenses exceed your predicted income. You need to review the 'Categorization' tab and cut down on non-essential spending."
        )
        
    if 'Working Hours' in daily_df.columns:
        recent_max_hours = daily_df['Working Hours'].tail(7).max() if not daily_df.empty else 0
        if recent_max_hours > 8:
            recommendations.append(
                "😴 **Burnout Warning:** You've had shifts exceeding 8 hours recently. Prolonged over-working decreases your hourly efficiency and increases risk. Prioritize heavy rest days soon!"
            )
    
    # Adaptive savings plan
    savings_rate = 0.2
    if volatility > (prediction * 0.4):
        savings_rate = 0.3 # Save more if highly volatile
        
    recommended_savings = prediction * savings_rate
    recommendations.append(
        f"💡 **Savings Plan:** Based on your current income trend, try to save **₹{recommended_savings:.2f}** tomorrow (approx {savings_rate * 100}% of predicted income)."
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
