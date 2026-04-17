import streamlit as st
import pandas as pd
import os
import datetime
import utils.data_processing as dp
import utils.categorization as cat
import utils.analysis as ana
import utils.visualization as vis
import utils.advisor as adv

# --- 1. LANGUAGE DICTIONARY ---
LANGUAGES = {
    "English": {
        "title": "Gig Worker AI Finance Coach", "dashboard_title": "📊 Financial Overview Dashboard",
        "total_income": "Total Income", "total_expenses": "Total Expenses", "net_savings": "Net Savings",
        "predicted_next_day": "Predicted Next Day", "tab1": "📈 Income & Lean Periods", "tab2": "📁 Expenses & Categorization",
        "tab3": "💡 Financial Recommendations", "tab4": "💬 AI Advisor", "goal_tracker": "🎯 Goal Tracking",
        "save_goal": "Save Goal", "login_title": "🔐 Private Vault Login"
    },
    "Tamil / தமிழ்": {
        "title": "கிக் ஒர்க்கர் AI நிதி பயிற்சியாளர்", "dashboard_title": "📊 நிதி மேலோட்ட மேடை",
        "total_income": "மொத்த வருமானம்", "total_expenses": "மொத்த செலவுகள்", "net_savings": "நிகர சேமிப்பு",
        "predicted_next_day": "அடுத்த நாள் கணிப்பு", "tab1": "📈 வருமானம் & குறைந்த காலம்", "tab2": "📁 செலவுகள் & வகைப்பாடு",
        "tab3": "💡 நிதி பரிந்துரைகள்", "tab4": "💬 AI ஆலோசகர்", "goal_tracker": "🎯 இலக்கு கண்காணிப்பு",
        "save_goal": "இலக்கை சேமி", "login_title": "🔐 தனிப்பட்ட நுழைவு"
    },
    "Urdu / اردو": {
        "title": "گِگ ورکر AI فنانس کوچ", "dashboard_title": "📊 مالیاتی جائزہ ڈیش بورڈ",
        "total_income": "کل آمدنی", "total_expenses": "کل اخراجات", "net_savings": "خالص بچت",
        "predicted_next_day": "اگلے دن کی پیشن گوئی", "tab1": "📈 آمدنی اور کم تر مدت", "tab2": "📁 اخراجات اور زمرہ بندی",
        "tab3": "💡 مالیاتی سفارشات", "tab4": "💬 AI مشیر", "goal_tracker": "🎯 ہدف سے باخبر رہنا",
        "save_goal": "ہدف محفوظ کریں", "login_title": "🔐 نجی لاگ ان"
    }
}

# --- 2. PRIVATE ISOLATION LOGIC ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

def get_user_data_file(u): return f"data_private_{u}.csv"
def get_user_profile_file(u): return f"profile_{u}.csv"

if not st.session_state.authenticated:
    st.set_page_config(page_title="Vault Login", layout="centered")
    st.title("🔐 Gig Worker Vault")
    t_login, t_signup = st.tabs(["Login", "Create Account"])
    with t_login:
        u = st.text_input("Username", key="l_u")
        p = st.text_input("Password", type="password", key="l_p")
        if st.button("Unlock"):
            db_path = "users_database.csv"
            if os.path.exists(db_path):
                users = pd.read_csv(db_path)
                if not users[(users['username'] == u) & (users['password'] == p)].empty:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Wrong info.")
    with t_signup:
        nu = st.text_input("New User")
        np = st.text_input("New Pass", type="password")
        fn = st.text_input("Your Name")
        if st.button("Register"):
            db_path = "users_database.csv"
            row = pd.DataFrame([{"username": nu, "password": np}])
            if os.path.exists(db_path):
                all_u = pd.read_csv(db_path)
                pd.concat([all_u, row]).to_csv(db_path, index=False)
            else: row.to_csv(db_path, index=False)
            pd.DataFrame([{"Name": fn}]).to_csv(get_user_profile_file(nu), index=False)
            st.success("Ready! Go to Login.")
    st.stop()

# --- 3. MAIN APP SETUP ---
USER_ID = st.session_state.username
LOCAL_SAVE_FILE = get_user_data_file(USER_ID)
if os.path.exists(get_user_profile_file(USER_ID)):
    user_name = pd.read_csv(get_user_profile_file(USER_ID)).iloc[0]['Name']
else: user_name = USER_ID

# Sidebar Setup
with st.sidebar:
    st.title(f"👤 {user_name}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("---")
    sel_lang = st.selectbox("Language / மொழி / اردو", list(LANGUAGES.keys()))
    t = LANGUAGES[sel_lang]
    input_method = st.radio("Input Data", ["Manual Entry", "Upload CSV"])
    uploaded_file = st.file_uploader("Upload CSV", type="csv") if input_method == "Upload CSV" else None

st.set_page_config(page_title=t["title"], layout="wide")

# Goal Logic
if "goals_df" not in st.session_state:
    st.session_state.goals_df = pd.read_csv("goals_history.csv") if os.path.exists("goals_history.csv") else pd.DataFrame(columns=["Goal Name", "Target", "Status", "Start Date"])

with st.sidebar:
    st.markdown("---")
    st.subheader(t["goal_tracker"])
    g_name = st.text_input("Goal Name")
    g_amt = st.number_input("Target (₹)", min_value=0.0)
    if st.button(t["save_goal"]):
        new_g = pd.DataFrame([{"Goal Name": g_name, "Target": g_amt, "Status": "Active", "Start Date": str(datetime.date.today())}])
        st.session_state.goals_df = pd.concat([st.session_state.goals_df, new_g])
        st.session_state.goals_df.to_csv("goals_history.csv", index=False)
        st.success("Goal Set!")

# Data Loading
if "manual_df" not in st.session_state:
    st.session_state.manual_df = pd.read_csv(LOCAL_SAVE_FILE) if os.path.exists(LOCAL_SAVE_FILE) else pd.DataFrame(columns=["Date", "Income", "Tips", "Working Hours", "Expense", "Category", "Description"])

if input_method == "Manual Entry":
    st.title("Financial Entry ✍️")
    edited = st.data_editor(st.session_state.manual_df, num_rows="dynamic", use_container_width=True)
    if st.button("Process & Save", type="primary"):
        edited.to_csv(LOCAL_SAVE_FILE, index=False)
        st.session_state.manual_df = edited
        st.rerun()

data_to_process = None
if input_method == "Manual Entry" and not st.session_state.manual_df.empty: data_to_process = st.session_state.manual_df
elif input_method == "Upload CSV" and uploaded_file: data_to_process = uploaded_file

if data_to_process is not None:
    df, _ = dp.load_and_clean_data(data_to_process)
    df = cat.apply_categorization(df)
    daily_df = ana.daily_aggregation(df)
    prediction, volatility = ana.predict_future_income(daily_df)
    lean_days, threshold = ana.detect_lean_periods(daily_df)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["total_income"], f"₹{df['Income'].sum() + df['Tips'].sum():,.2f}")
    c2.metric(t["total_expenses"], f"₹{df['Expense'].sum():,.2f}")
    c3.metric(t["net_savings"], f"₹{(df['Income'].sum()+df['Tips'].sum()) - df['Expense'].sum():,.2f}")
    c4.metric(t["predicted_next_day"], f"₹{prediction:,.2f}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], "🏆 History"])
    with tab1:
        st.plotly_chart(vis.plot_income_trend(daily_df, lean_days, threshold), use_container_width=True)
    with tab3:
        st.subheader(t["tab3"])
        for r in adv.generate_recommendations(daily_df, prediction, volatility): st.info(r)
    with tab4:
        st.subheader(t["tab4"])
        q = st.text_input("Ask Question")
        if st.button("Ask"): st.success(adv.ai_financial_response(q, daily_df))
    with tab5:
        st.subheader("Goal Wall of Fame")
        st.dataframe(st.session_state.goals_df)




