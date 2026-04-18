import streamlit as st
import pandas as pd
import os
import datetime
import utils.data_processing as dp
import utils.categorization as cat
import utils.analysis as ana
import utils.visualization as vis
import utils.advisor as adv

# --- 1. LANGUAGE DICTIONARY (7 LANGUAGES) ---
LANGUAGES = {
    "English": {"title": "Gig Worker Coach", "dashboard_title": "👑 Financial Dashboard", "total_income": "Total Income", "total_expenses": "Total Expenses", "net_savings": "Net Savings", "predicted_next_day": "Predicted Next Day", "tab1": "📈 Income Trends", "tab2": "📁 Categories", "tab3": "💡 AI Recommendations", "tab4": "💬 Chatbot", "goal_tracker": "🎯 Goal Tracking", "save_goal": "Save Goal", "save_data": "Save Data for Later 💾", "process": "Process Data 🚀"},
    "Tamil / தமிழ்": {"title": "AI நிதி பயிற்சியாளர்", "dashboard_title": "👑 நிதி மேலோட்ட மேடை", "total_income": "மொத்த வருமானம்", "total_expenses": "மொத்த செலவுகள்", "net_savings": "நிகர சேமிப்பு", "predicted_next_day": "அடுத்த நாள் கணிப்பு", "tab1": "📈 வருமானப் போக்கு", "tab2": "📁 வகைகள்", "tab3": "💡 AI பரிந்துரைகள்", "tab4": "💬 உரையாடல்", "goal_tracker": "🎯 இலக்கு", "save_goal": "இலக்கை சேமி", "save_data": "தரவைச் சேமி 💾", "process": "செயலாக்கு 🚀"},
    "Hindi / हिन्दी": {"title": "AI फाइनेंस कोच", "dashboard_title": "👑 वित्तीय अवलोकन", "total_income": "कुल आय", "total_expenses": "कुल खर्च", "net_savings": "शुद्ध बचत", "predicted_next_day": "अगले दिन का अनुमान", "tab1": "📈 आय का रुझान", "tab2": "📁 श्रेणियाँ", "tab3": "💡 AI सिफारिशें", "tab4": "💬 चैटबॉट", "goal_tracker": "🎯 लक्ष्य ट्रैकिंग", "save_goal": "लक्ष्य सहेजें", "save_data": "डेटा सहेजें 💾", "process": "प्रोसेस करें 🚀"},
    "Urdu / اردو": {"title": "فنانس کوچ", "dashboard_title": "👑 مالیاتی جائزہ", "total_income": "کل آمدنی", "total_expenses": "کل اخراجات", "net_savings": "خالص بچت", "predicted_next_day": "اگلے دن کی پیشن گوئی", "tab1": "📈 رجحانات", "tab2": "📁 زمرہ جات", "tab3": "💡 سفارشات", "tab4": "💬 چیٹ بوٹ", "goal_tracker": "🎯 ہدف کا سراغ لگانا", "save_goal": "ہدف محفوظ کریں", "save_data": "ڈیٹا محفوظ کریں 💾", "process": "عمل درآمد 🚀"},
    "Telugu / తెలుగు": {"title": "AI ఆర్థిక కోచ్", "dashboard_title": "👑 ఆర్థిక అవలోకనం", "total_income": "మొత్తం ఆదాయం", "total_expenses": "మొత్తం ఖర్చులు", "net_savings": "నికర పొదుపు", "predicted_next_day": "తర్వాతి రోజు అంచనా", "tab1": "📈 ధోరణులు", "tab2": "📁 వర్గాలు", "tab3": "💡 సిఫార్సులు", "tab4": "💬 చాట్‌బాట్", "goal_tracker": "🎯 లక్ష్యం", "save_goal": "లక్ష్యాన్ని సేవ్ చేయండి", "save_data": "డేటాను సేవ్ చేయి 💾", "process": "ప్రాసెస్ చేయండి 🚀"},
    "Kannada / ಕನ್ನಡ": {"title": "AI ಹಣಕಾಸು ತರಬೇತುದಾರ", "dashboard_title": "👑 ಆರ್ಥಿಕ ಅವಲೋಕನ", "total_income": "ಒಟ್ಟು ಆದಾಯ", "total_expenses": "ಒಟ್ಟು ವೆಚ್ಚಗಳು", "net_savings": "ನಿವ್ವಳ ಉಳಿತಾಯ", "predicted_next_day": "ಮುಂದಿನ ದಿನದ ಮುನ್ಸೂಚನೆ", "tab1": "📈 ಪ್ರವೃತ್ತಿಗಳು", "tab2": "📁 ವರ್ಗಗಳು", "tab3": "💡 ಶಿಫಾರಸುಗಳು", "tab4": "💬 ಚಾಟ್‌ಬಾಟ್", "goal_tracker": "🎯 ಗುರಿ", "save_goal": "ಗುರಿ ಉಳಿಸಿ", "save_data": "ಉಳಿಸಿ 💾", "process": "ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಿ 🚀"},
    "Malayalam / മലയാളം": {"title": "AI ഫിനാൻസ് കോച്ച്", "dashboard_title": "👑 സാമ്പത്തിക അവലോകനം", "total_income": "ആകെ വരുമാനം", "total_expenses": "ആകെ ചെലവുകൾ", "net_savings": "അറ്റാദായം", "predicted_next_day": "അടുത്ത ദിവസത്തെ പ്രവചനം", "tab1": "📈 ട്രെൻഡുകൾ", "tab2": "📁 വിഭാഗങ്ങൾ", "tab3": "💡 ശുപാർശകൾ", "tab4": "💬 ചാറ്റ്ബോട്ട്", "goal_tracker": "🎯 ലക്ഷ്യം", "save_goal": "ലക്ഷ്യം സേവ് ചെയ്യുക", "save_data": "സേവ് ചെയ്യുക 💾", "process": "പ്രോസസ്സ് ചെയ്യുക 🚀"}
}

# --- 2. AUTH LOGIC ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

def get_user_data_file(u): return f"data_private_{u}.csv"
def get_user_profile_file(u): return f"profile_{u}.csv"

if not st.session_state.authenticated:
    st.set_page_config(page_title="Vault Login", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>💎 Gig Worker Private Vault</h1>", unsafe_allow_html=True)
    t_login, t_signup = st.tabs(["Login", "Create Account"])
    with t_login:
        u = st.text_input("Username", key="l_u")
        p = st.text_input("Password", type="password", key="l_p")
        if st.button("Unlock Vault 🔑"):
            db_path = "users_database.csv"
            if os.path.exists(db_path):
                users = pd.read_csv(db_path)
                if not users[(users['username'] == u) & (users['password'] == p)].empty:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Incorrect username or password.")
            else:
                st.info("No accounts found on this server yet. Please click 'Create Account' to get started!")
    with t_signup:
        nu = st.text_input("Choose Username")
        np = st.text_input("Choose Password", type="password")
        fn = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        job = st.selectbox("Job / Gig Type", ["Delivery Partner", "Ride-share Driver", "Freelancer", "Manual Labor", "Other"])
        
        if st.button("Create My Vault"):
            db_path = "users_database.csv"
            row = pd.DataFrame([{"username": nu, "password": np}])
            if os.path.exists(db_path):
                all_u = pd.read_csv(db_path)
                pd.concat([all_u, row]).to_csv(db_path, index=False)
            else: row.to_csv(db_path, index=False)
            
            # Save Full Profile
            profile_data = {
                "Name": fn,
                "Age": age,
                "Gender": gender,
                "Job": job,
                "Joined": str(datetime.date.today())
            }
            pd.DataFrame([profile_data]).to_csv(get_user_profile_file(nu), index=False)
            st.success("Vault Created! You can now login.")
    st.stop()

# --- 3. MAIN APP ---
USER_ID = st.session_state.username
LOCAL_SAVE_FILE = get_user_data_file(USER_ID)
PROFILE_FILE = get_user_profile_file(USER_ID)

if os.path.exists(PROFILE_FILE):
    user_bio = pd.read_csv(PROFILE_FILE).iloc[0]
else:
    user_bio = {"Name": USER_ID, "Age": "N/A", "Gender": "N/A", "Job": "N/A"}

# Sidebar Setup
with st.sidebar:
    st.markdown(f"""
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h2 style="margin:0;">👑 {user_bio['Name']}</h2>
            <p style="margin:5px 0; color: #64748b;">💼 {user_bio['Job']}</p>
            <p style="margin:0; font-size: 0.9em;">🎂 {user_bio['Age']} years | ⚧ {user_bio['Gender']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Exit Vault"):
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("---")
    sel_lang = st.selectbox("Language / மொழி", list(LANGUAGES.keys()))
    t = LANGUAGES[sel_lang]
    input_method = st.radio("Input Mode", ["Manual Entry", "Upload CSV"])
    uploaded_file = st.file_uploader("Upload CSV", type="csv") if input_method == "Upload CSV" else None

st.set_page_config(page_title=t["title"], layout="wide")

# Goal Data
if "goals_df" not in st.session_state:
    st.session_state.goals_df = pd.read_csv("goals_history.csv") if os.path.exists("goals_history.csv") else pd.DataFrame(columns=["Goal", "Target", "Status", "Start Date"])

with st.sidebar:
    st.markdown("---")
    st.subheader(t["goal_tracker"])
    g_n, g_a = st.text_input("Goal Name"), st.number_input("Target (₹)", min_value=0.0)
    if st.button(t["save_goal"]):
        new_g = pd.DataFrame([{"Goal": g_n, "Target": g_a, "Status": "Active", "Start Date": str(datetime.date.today())}])
        st.session_state.goals_df = pd.concat([st.session_state.goals_df, new_g], ignore_index=True)
        st.session_state.goals_df.to_csv("goals_history.csv", index=False)
        st.success("Set!")

# Manual Entry with Calendar
if "manual_df" not in st.session_state:
    if os.path.exists(LOCAL_SAVE_FILE):
        st.session_state.manual_df = pd.read_csv(LOCAL_SAVE_FILE)
        st.session_state.manual_df['Date'] = pd.to_datetime(st.session_state.manual_df['Date'])
    else:
        st.session_state.manual_df = pd.DataFrame(columns=["Date", "Income", "Tips", "Working Hours", "Expense", "Category", "Description"])

if input_method == "Manual Entry":
    st.title("Financial Entry ✍️")
    col_config = {
        "Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY", required=True),
        "Income": st.column_config.NumberColumn("Income (₹)", min_value=0), "Tips": st.column_config.NumberColumn("Tips (₹)", min_value=0),
        "Expense": st.column_config.NumberColumn("Expense (₹)", min_value=0), "Category": st.column_config.SelectboxColumn("Category", options=["Food", "Fuel", "Rent", "Bills", "Others"])
    }
    ed = st.data_editor(st.session_state.manual_df, column_config=col_config, num_rows="dynamic", use_container_width=True)
    c_p, c_s = st.columns(2)
    if c_p.button(t["process"], type="primary"): st.session_state.manual_df = ed
    if c_s.button(t["save_data"]): ed.to_csv(LOCAL_SAVE_FILE, index=False); st.success("Saved!")

# Visuals
data = None
if input_method == "Manual Entry" and not st.session_state.manual_df.empty: data = st.session_state.manual_df
elif input_method == "Upload CSV" and uploaded_file: data = uploaded_file

if data is not None:
    df, err = dp.load_and_clean_data(data)
    if err: st.error(err)
    else:
        df = cat.apply_categorization(df)
        daily_df = ana.daily_aggregation(df)
        pred, vol = ana.predict_future_income(daily_df)
        lean, thresh = ana.detect_lean_periods(daily_df)

        st.title(t["dashboard_title"])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(t["total_income"], f"₹{df['Income'].sum()+df['Tips'].sum():,.0f}", delta="Income")
        m2.metric(t["total_expenses"], f"₹{df['Expense'].sum():,.0f}", delta="Costs", delta_color="inverse")
        m3.metric(t["net_savings"], f"₹{(df['Income'].sum()+df['Tips'].sum())-df['Expense'].sum():,.0f}", delta="Profit")
        m4.metric(t["predicted_next_day"], f"₹{pred:,.0f}")

        t1, t2, t3, t4, t5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], "🏆 History"])
        with t1:
            fig_t = vis.plot_income_trend(daily_df, lean, thresh)
            if fig_t: st.plotly_chart(fig_t, use_container_width=True)
        with t2:
            fig_p = vis.plot_expense_distribution(df)
            if fig_p: st.plotly_chart(fig_p, use_container_width=True)
        with t3:
            for r in adv.generate_recommendations(daily_df, pred, vol):
                if "🚨" in r or "🚩" in r: st.error(r)
                elif "✅" in r or "🚀" in r: st.success(r)
                else: st.info(r)
        with t4:
            q = st.text_input("Ask Anything")
            if st.button("Ask"): st.warning(adv.ai_financial_response(q, daily_df))
        with t5: st.dataframe(st.session_state.goals_df, use_container_width=True, hide_index=True)
else:
    st.markdown('<div style="background-color: #f0f7ff; padding: 30px; border-radius: 15px; border-left: 10px solid #1e3a8a;"><h1 style="color: #1e3a8a;">👋 Welcome!</h1><p style="font-size: 18px;">Master your Gig Earnings with ease.</p><p>👈 Use the sidebar to enter your data.</p></div>', unsafe_allow_html=True)
