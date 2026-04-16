import streamlit as st
import pandas as pd
import utils.data_processing as dp
import utils.categorization as cat
import utils.analysis as ana
import utils.visualization as vis
import utils.advisor as adv

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Gig Worker AI Finance Coach",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2ecc71;
    }
    .metric-label {
        font-size: 1rem;
        color: #bdc3c7;
    }
    .warning-box {
        background-color: #e74c3c22;
        border-left: 5px solid #e74c3c;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


import datetime

TRANS = {
    "English": {
        "title": "AI Finance Coach",
        "input_method": "How do you want to input your data?",
        "upload": "Upload CSV",
        "manual": "Manual Entry",
        "goal_tracker": "🎯 Goal Tracking",
        "goal_name": "Goal Name",
        "goal_amount": "Target Amount (₹)",
        "save_goal": "Save Goal",
        "saved_success": "Saved!",
        "total_income": "Total Income",
        "total_expenses": "Total Expenses",
        "net_savings": "Net Savings",
        "dashboard_title": "📊 Financial Overview Dashboard",
        "predicted_next_day": "Predicted Next Day",
        "tab1": "📈 Income & Lean Periods",
        "tab2": "🛒 Expenses & Categorization",
        "tab3": "💡 Financial Recommendations",
        "tab4": "🤖 AI Advisor",
        "tab2_hd": "Intelligent Expense Categorization",
        "tab2_sub": "Your expenses are automatically categorized using natural language processing on transaction descriptions.",
        "tab2_top": "**Top Transactions:**"
    },
    "Hindi (हिंदी)": {
        "title": "एआई फाइनेंस",
        "input_method": "अपना डेटा दर्ज करें",
        "upload": "CSV अपलोड करें",
        "manual": "मैन्युअल प्रविष्टि",
        "goal_tracker": "🎯 वित्तीय लक्ष्य",
        "goal_name": "लक्ष्य का नाम",
        "goal_amount": "लक्ष्य राशि (₹)",
        "save_goal": "सहेजें",
        "saved_success": "सहेजा गया!",
        "total_income": "कुल आय",
        "total_expenses": "कुल व्यय",
        "net_savings": "शुद्ध बचत",
        "dashboard_title": "📊 वित्तीय डैशबोर्ड",
        "predicted_next_day": "अनुमानित आय",
        "tab1": "📈 आय रुझान",
        "tab2": "🛒 व्यय वर्गीकरण",
        "tab3": "💡 वित्तीय सुझाव",
        "tab4": "🤖 एआई सलाहकार",
        "tab2_hd": "बुद्धिमान व्यय वर्गीकरण",
        "tab2_sub": "आपके खर्च स्वचालित रूप से वर्गीकृत होते हैं।",
        "tab2_top": "**शीर्ष लेनदेन:**"
    },
    "Tamil (தமிழ்)": {
        "title": "ஏஐ பைனான்ஸ்",
        "input_method": "தரவை எவ்வாறு உள்ளிடுவீர்கள்?",
        "upload": "CSV பதிவேற்று",
        "manual": "மேனுவல்",
        "goal_tracker": "🎯 நிதி இலக்குகள்",
        "goal_name": "இலக்கின் பெயர்",
        "goal_amount": "இலக்குத் தொகை (₹)",
        "save_goal": "சேமி",
        "saved_success": "சேமிக்கப்பட்டது!",
        "total_income": "மொத்த வருமானம்",
        "total_expenses": "மொத்த செலவுகள்",
        "net_savings": "நிகர சேமிப்பு",
        "dashboard_title": "📊 நிதி கண்ணோட்டம்",
        "predicted_next_day": "எதிர்பார்க்கப்படும் வருமானம்",
        "tab1": "📈 வருமான விவரங்கள்",
        "tab2": "🛒 செலவுகள்",
        "tab3": "💡 நிதி ஆலோசனைகள்",
        "tab4": "🤖 ஏஐ வழிகாட்டி",
        "tab2_hd": "செலவு வகைப்படுத்தல்",
        "tab2_sub": "உங்கள் செலவுகள் தானாகவே வகைப்படுத்தப்படும்.",
        "tab2_top": "**முக்கிய பரிவர்த்தனைகள்:**"
    },
    "Urdu (اردو)": {
        "title": "اے آئی فنانس",
        "input_method": "اپنا ڈیٹا درج کریں",
        "upload": "CSV اپ لوڈ",
        "manual": "دستی اندراج",
        "goal_tracker": "🎯 مالیاتی اہداف",
        "goal_name": "ہدف کا نام",
        "goal_amount": "ہدف کی رقم (₹)",
        "save_goal": "محفوظ کریں",
        "saved_success": "محفوظ ہو گیا!",
        "total_income": "کل آمدنی",
        "total_expenses": "کل اخراجات",
        "net_savings": "خالص بچت",
        "dashboard_title": "📊 مالیاتی ڈیش بورڈ",
        "predicted_next_day": "متوقع آمدنی",
        "tab1": "📈 آمدنی کے رجحانات",
        "tab2": "🛒 اخراجات کی زمرہ بندی",
        "tab3": "💡 مالیاتی تجاویز",
        "tab4": "🤖 اے آئی ایڈوائزر",
        "tab2_hd": "ذہین اخراجات کی درجہ بندی",
        "tab2_sub": "آپ کے اخراجات خود بخود درجہ بندی کیے جاتے ہیں۔",
        "tab2_top": "**اہم لین دین:**"
    },
    "Telugu (తెలుగు)": {
        "title": "ఏఐ ఫైనాన్స్",
        "input_method": "డేటా ఎంట్రీ",
        "upload": "CSV అప్‌లోడ్",
        "manual": "మాన్యువల్ ఎంట్రీ",
        "goal_tracker": "🎯 ఆర్ధిక లక్ష్యాలు",
        "goal_name": "లక్ష్యం పేరు",
        "goal_amount": "లక్ష్యం మొత్తం (₹)",
        "save_goal": "దాచు",
        "saved_success": "దాచినది!",
        "total_income": "ఆదాయం",
        "total_expenses": "ఖర్చులు",
        "net_savings": "పొదుపు",
        "dashboard_title": "📊 కంట్రోల్ ప్యానెల్",
        "predicted_next_day": "అంచనా ఆదాయం",
        "tab1": "📈 ఆదాయం వివరాలు",
        "tab2": "🛒 ఖర్చుల విభజన",
        "tab3": "💡 ఆర్ధిక సూచనలు",
        "tab4": "🤖 సలహాదారు",
        "tab2_hd": "ఖర్చుల వర్గీకరణ",
        "tab2_sub": "మీ ఖర్చులు స్వయంచాలకంగా వర్గీకరించబడతాయి.",
        "tab2_top": "**ముఖ్యమైన లావాదేవీలు:**"
    },
    "Kannada (ಕನ್ನಡ)": {
        "title": "ಎಐ ಫೈನಾನ್ಸ್",
        "input_method": "ಡೇಟಾವನ್ನು ನಮೂದಿಸಿ",
        "upload": "CSV ಅಪ್‌ಲೋಡ್",
        "manual": "ಮ್ಯಾನುಯಲ್ ಎಂಟ್ರಿ",
        "goal_tracker": "🎯 ಗುರಿಗಳು",
        "goal_name": "ಗುರಿಯ ಹೆಸರು",
        "goal_amount": "ಗುರಿಯ ಮೊತ್ತ (₹)",
        "save_goal": "ಉಳಿಸಿ",
        "saved_success": "ಉಳಿಸಲಾಗಿದೆ!",
        "total_income": "ಆದಾಯ",
        "total_expenses": "ಖರ್ಚು",
        "net_savings": "ಉಳಿತಾಯ",
        "dashboard_title": "📊 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "predicted_next_day": "ನಿರೀಕ್ಷಿತ ಆದಾಯ",
        "tab1": "📈 ಆದಾಯದ ವಿವರಗಳು",
        "tab2": "🛒 ಖರ್ಚು ವರ್ಗೀಕರಣ",
        "tab3": "💡 ಆರ್ಥಿಕ ಸಲಹೆಗಳು",
        "tab4": "🤖 ಎಐ ಸಲಹೆಗಾರ",
        "tab2_hd": "ಖರ್ಚಿನ ವರ್ಗೀಕರಣ",
        "tab2_sub": "ನಿಮ್ಮ ಖರ್ಚುಗಳನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ವರ್ಗೀಕರಿಸಲಾಗುತ್ತದೆ.",
        "tab2_top": "**ಟಾಪ್ ವಹಿವಾಟುಗಳು:**"
    },
    "Malayalam (മലയാളം)": {
        "title": "എഐ ഫിനാൻസ്",
        "input_method": "ഡാറ്റ നൽകുക",
        "upload": "CSV അപ്‌ലോഡ്",
        "manual": "മാനുവൽ",
        "goal_tracker": "🎯 ലക്ഷ്യങ്ങൾ",
        "goal_name": "ലക്ഷ്യം",
        "goal_amount": "ലക്ഷ്യ തുക (₹)",
        "save_goal": "സംരക്ഷിക്കുക",
        "saved_success": "സരക്ഷിച്ചു!",
        "total_income": "വരുമാനം",
        "total_expenses": "ചെലവുകൾ",
        "net_savings": "അറ്റ നിക്ഷേപം",
        "dashboard_title": "📊 സാമ്പത്തിക ഡാഷ്ബോർഡ്",
        "predicted_next_day": "പ്രതീക്ഷിക്കുന്ന വരുമാനം",
        "tab1": "📈 വരുമാനം",
        "tab2": "🛒 ചെലവുകൾ",
        "tab3": "💡 നിർദ്ദേശങ്ങൾ",
        "tab4": "🤖 ഉപദേഷ്ടാവ്",
        "tab2_hd": "ചെലവ് വർഗ്ഗീകരണം",
        "tab2_sub": "നിങ്ങളുടെ ചെലവുകൾ സ്വയം വർഗ്ഗീകരിക്കുന്നു.",
        "tab2_top": "**പ്രധാന ഇടപാടുകൾ:**"
    }
}


# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    
    language = st.selectbox("Language / மொழி / زبان / భాష / ಭಾಷೆ / ഭാഷ", list(TRANS.keys()))
    t = TRANS[language]
    
    st.title(t["title"])
    st.markdown(t["input_method"])
    
    # Internal mappings
    radio_opts = {t["upload"]: "Upload CSV", t["manual"]: "Manual Entry"}
    input_method_display = st.radio("Method", list(radio_opts.keys()), label_visibility="collapsed")
    input_method = radio_opts[input_method_display]
    
    # Goal Setting Logic
    st.markdown("---")
    st.subheader(t["goal_tracker"])
    
    if "goals_df" not in st.session_state:
        import os
        if os.path.exists("goals_history.csv"):
            st.session_state.goals_df = pd.read_csv("goals_history.csv")
        else:
            st.session_state.goals_df = pd.DataFrame(columns=["Goal Name", "Target Amount", "Status", "Start Date", "Completed Date", "Days Taken"])
            
    if 'goal_name' not in st.session_state:
        st.session_state['goal_name'] = ""
    if 'goal_amount' not in st.session_state:
        st.session_state['goal_amount'] = 0.0
        
    g_name = st.text_input(t["goal_name"], value=st.session_state['goal_name'])
    g_amt = st.number_input(t["goal_amount"], min_value=0.0, step=500.0, value=float(st.session_state['goal_amount']))
    g_start = st.date_input("Start Date", value=datetime.date.today())
    
    if st.button(t["save_goal"]):
        st.session_state['goal_name'] = g_name
        st.session_state['goal_amount'] = g_amt
        st.session_state['goal_start'] = g_start.strftime("%Y-%m-%d")
        
        # Check if goal exists in history, if not add it
        existing = st.session_state.goals_df[st.session_state.goals_df["Goal Name"] == g_name]
        if existing.empty:
            new_row = pd.DataFrame([{
                "Goal Name": g_name, 
                "Target Amount": g_amt, 
                "Status": "Active", 
                "Start Date": g_start.strftime("%Y-%m-%d"), 
                "Completed Date": "",
                "Days Taken": 0
            }])
            st.session_state.goals_df = pd.concat([st.session_state.goals_df, new_row], ignore_index=True)
            st.session_state.goals_df.to_csv("goals_history.csv", index=False)
            
        st.success(t["saved_success"])
    
    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("CSV (Date, Income, Tips, Working Hours, Expense, Description)", type=["csv"])
    else:
        uploaded_file = None
        
    st.markdown("---")
    st.markdown("**Gig Worker Toolkit v1.0**")


# --- MAIN LOGIC ---
data_to_process = None

if input_method == "Upload CSV" and uploaded_file is None:
    st.title("Welcome to your Personal AI Finance Coach! 💼")
    st.markdown("""
        As a gig worker, your income fluctuates. This app helps you:
        - **Track** your income and expenses over time.
        - **Categorize** your spending automatically.
        - **Predict** future income and detect lean periods.
        - **Receive** personalized financial advice.
        
        👉 **Please upload a CSV file in the sidebar to begin.**
        
        *Expected CSV Format:*
        `Date, Income, Tips, Working Hours, Expense, Description`
    """)
elif input_method == "Manual Entry":
    st.title("Enter Your Finances Manually ✍️")
    st.markdown("Add your transactions below. The dashboard will update automatically when you click Process.")
    st.markdown("*(Tip: To delete a specific row, click the row number on the far left to highlight it, then press the `Delete` key on your keyboard!)*")
    
    LOCAL_SAVE_FILE = "saved_finances.csv"
    
    if "manual_df" not in st.session_state or "Working Hours" not in st.session_state.manual_df.columns:
        import os
        if os.path.exists(LOCAL_SAVE_FILE):
            saved_df = pd.read_csv(LOCAL_SAVE_FILE)
            if 'Date' in saved_df.columns:
                saved_df['Date'] = pd.to_datetime(saved_df['Date'], errors='coerce')
                
            # Ensure new columns exist in old saves
            if 'Working Hours' not in saved_df.columns:
                saved_df['Working Hours'] = 0.0
                
            st.session_state.manual_df = saved_df
        else:
            st.session_state.manual_df = pd.DataFrame(columns=[
                "Date", "Income", "Tips", "Working Hours", "Expense", "Category", "Description"
            ])
            st.session_state.manual_df['Date'] = pd.to_datetime(st.session_state.manual_df['Date'])
        
    edited_df = st.data_editor(
        st.session_state.manual_df,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
            "Income": st.column_config.NumberColumn("Income (₹)", format="₹%.0f"),
            "Tips": st.column_config.NumberColumn("Tips (₹)", format="₹%.0f"),
            "Working Hours": st.column_config.NumberColumn("Hours", format="%.1f"),
            "Expense": st.column_config.NumberColumn("Expense (₹)", format="₹%.0f"),
            "Category": st.column_config.SelectboxColumn("Category", options=["Food", "Rent", "Travel", "Bills", "Entertainment", "Fuel", "Others"]),
        },
        num_rows="dynamic",
        use_container_width=True
    )
    
    colA, colB = st.columns(2)
    with colA:
        process_btn = st.button("Process Manual Data", type="primary")
    with colB:
        save_btn = st.button("Save Data for Later 💾")
        
    if process_btn:
        st.session_state.process_manual = True
        st.session_state.manual_df = edited_df
        
    if save_btn:
        edited_df.to_csv(LOCAL_SAVE_FILE, index=False)
        st.success("Your data has been successfully saved! It will load automatically next time.")
        st.session_state.process_manual = True
        st.session_state.manual_df = edited_df

    if st.session_state.get("process_manual", False):
        data_to_process = edited_df
elif input_method == "Upload CSV" and uploaded_file is not None:
    data_to_process = uploaded_file

if data_to_process is not None:
    # 1. Data Ingestion
    with st.spinner("Processing Data..."):
        df, error = dp.load_and_clean_data(data_to_process)
        
    if error:
        st.error(error)
    else:
        # 2. Categorization
        df = cat.apply_categorization(df)
        
        # 3. Time Series Analysis
        daily_df = ana.daily_aggregation(df)
        prediction, volatility = ana.predict_future_income(daily_df)
        lean_days, threshold = ana.detect_lean_periods(daily_df)
        
        
        # --- UI LAYOUT ---
        st.title(t["dashboard_title"])
        
        # Calculate Goals Component
        total_income = df['Income'].sum() + df['Tips'].sum()
        total_expense = df['Expense'].sum()
        savings = total_income - total_expense
        
        nav_g_name = st.session_state.get('goal_name', '')
        nav_g_amt = st.session_state.get('goal_amount', 0.0)
        
        if nav_g_name and nav_g_amt > 0:
            st.markdown(f"### 🎯 Progress: {nav_g_name}")
            prog_val = min(savings / nav_g_amt, 1.0) if savings > 0 else 0.0
            
            col_bar, col_text = st.columns([4, 1])
            with col_bar:
                st.progress(prog_val)
            with col_text:
                st.markdown(f"**{prog_val * 100:.1f}%**")
                
            col_msg, col_btn = st.columns([3, 1])
            with col_msg:
                st.markdown(f"***₹{savings:,.2f} tracking towards your ₹{nav_g_amt:,.2f} goal!***")
                
            if prog_val >= 1.0:
                with col_btn:
                    if st.button("✅ Mark Completed"):
                        idx = st.session_state.goals_df[st.session_state.goals_df['Goal Name'] == nav_g_name].index
                        if not idx.empty:
                            start_str = st.session_state.goals_df.loc[idx[0], 'Start Date']
                            start_d = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
                            end_d = datetime.date.today()
                            st.session_state.goals_df.loc[idx[0], 'Status'] = 'Completed'
                            st.session_state.goals_df.loc[idx[0], 'Completed Date'] = end_d.strftime("%Y-%m-%d")
                            st.session_state.goals_df.loc[idx[0], 'Days Taken'] = (end_d - start_d).days
                            st.session_state.goals_df.to_csv("goals_history.csv", index=False)
                        st.session_state['goal_name'] = ""
                        st.session_state['goal_amount'] = 0.0
                        st.rerun()
                        
            st.markdown("<br>", unsafe_allow_html=True)
            
        # Top Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"<div class='metric-label'>{t['total_income']}</div><div class='metric-value'>₹{total_income:,.2f}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-label'>{t['total_expenses']}</div><div class='metric-value' style='color:#e74c3c;'>₹{total_expense:,.2f}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-label'>{t['net_savings']}</div><div class='metric-value' style='color:#3498db;'>₹{savings:,.2f}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-label'>{t['predicted_next_day']}</div><div class='metric-value' style='color:#f39c12;'>₹{prediction:,.2f}</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], "🏆 History"])
        
        with tab1:
            st.subheader("Income Trends and Lean Period Detection")
            st.markdown("We analyze your daily aggregates to spot 'lean periods' where income drops below a dynamically calculated threshold (80% of mean).")
            
            # Plotly Line Chart
            fig_trend = vis.plot_income_trend(daily_df, lean_days, threshold)
            st.plotly_chart(fig_trend, use_container_width=True)
            
            if not lean_days.empty:
                st.markdown("<div class='warning-box'><strong>Alert:</strong> We detected lean periods in your history. Review the red markers on the chart and ensure your emergency fund covers these dips.</div>", unsafe_allow_html=True)
                
            with st.expander("View Daily Data Breakdown"):
                st.dataframe(daily_df, use_container_width=True)
                
        with tab2:
            st.subheader(t["tab2_hd"])
            st.markdown(t["tab2_sub"])
            
            col_a, col_b = st.columns([2, 1])
            with col_a:
                fig_pie = vis.plot_expense_distribution(df)
                if fig_pie:
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No expenses recorded yet.")
            with col_b:
                st.markdown(t["tab2_top"])
                top_expenses = df.sort_values(by='Expense', ascending=False).head(5)[['Date', 'Description', 'Expense', 'Category']]
                st.dataframe(top_expenses, hide_index=True)
                
        with tab3:
            st.subheader("Financial Insights & Recommendations")
            recs = adv.generate_recommendations(daily_df, prediction, volatility)
            
            for rec in recs:
                if 'Warning' in rec or 'Deficit' in rec or 'Risk' in rec:
                    st.warning(rec)
                elif 'Met' in rec:
                    st.success(rec)
                else:
                    st.info(rec)
                
            st.markdown("---")
            st.markdown("### 🏛️ Comprehensive Tax Estimation")
            total_tax_liability = total_income * 0.25
            recent_tax = (daily_df['Income'].iloc[-1] if not daily_df.empty else 0) * 0.25
            
            st.write(f"As an independent gig worker, your taxes are typically not withheld automatically from your payouts. It is strongly recommended to reserve around **20-25%** of your **Gross Income** to cover End-of-Year income tax and self-employment taxes.")
            
            st.info(f"**Total Estimated Tax Liability:** Based on your total logged income of ₹{total_income:,.2f}, you should have approximately **₹{total_tax_liability:,.2f}** sitting in a separate bank account exclusively for taxes.")
            st.warning(f"**Daily Tax Set-Aside:** Based on your most recent logged shift, put **₹{recent_tax:,.2f}** into your tax envelope immediately today so you don't fall behind.")
                
            st.markdown("---")
            st.markdown("### 🏛️ The 50/30/20 Budget Breakdown")
            st.write("A popular budgeting strategy recommends splitting your total income into Needs (50%), Wants (30%), and Savings (20%). Here are your personalized targets:")
            c_needs, c_wants, c_save = st.columns(3)
            with c_needs:
                st.success(f"**50% Essential Needs:**\n\n**₹{total_income * 0.50:,.2f}**")
            with c_wants:
                st.info(f"**30% Personal Wants:**\n\n**₹{total_income * 0.30:,.2f}**")
            with c_save:
                st.warning(f"**20% Future Savings:**\n\n**₹{total_income * 0.20:,.2f}**")

        with tab4:
            st.subheader("Ask the AI Financial Advisor")
            st.markdown("Ask any questions regarding your finances, taxes, or budgeting strategies.")
            
            user_question = st.text_input("Your Question:", placeholder="e.g., How much should I save for an emergency?")
            
            if st.button("Ask"):
                if user_question:
                    with st.spinner("Thinking..."):
                        # Simulating AI response with some delay for UX
                        import time
                        time.sleep(1)
                        if hasattr(adv, 'ai_financial_response'):
                            response = adv.ai_financial_response(user_question, daily_df)
                        else:
                            response = adv.get_chatbot_response(user_question, df, daily_df)
                        
                    st.success("**Advisor:** " + response)
                else:
                    st.warning("Please enter a question.")
                    
        with tab5:
            st.subheader("Your Goal Achievements & Time Spans")
            st.markdown("Review your past goals and analyze exactly how many days it took you to hit your savings milestones.")
            if "goals_df" in st.session_state and not st.session_state.goals_df.empty:
                st.dataframe(
                    st.session_state.goals_df.style.applymap(
                        lambda val: 'color: green; font-weight: bold' if val == 'Completed' else 'color: orange',
                        subset=['Status']
                    ),
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.info("No goals tracked yet! Enter a goal in the sidebar to get started.")
