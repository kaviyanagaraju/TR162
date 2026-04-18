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
    "English": {"title": "Gig Worker Coach", "dashboard_title": "👑 Financial Dashboard", "tab1": "📈 Income Trends", "tab2": "📁 Categories", "tab3": "💡 AI Recommendations", "tab4": "💬 Chatbot", "save_data": "Save Data💾", "total_income": "Total Income", "total_expenses": "Total Expenses", "net_savings": "Net Savings", "predicted_next_day": "Predicted Next Day"},
    "Tamil / தமிழ்": {"title": "AI நிதி பயிற்சியாளர்", "dashboard_title": "👑 நிதி மேலோட்ட மேடை", "tab1": "📈 வருமானப் போக்கு", "tab2": "📁 வகைகள்", "tab3": "💡 AI பரிந்துரைகள்", "tab4": "💬 உரையாடல்", "save_data": "சேமி 💾", "total_income": "மொத்த வருமானம்", "total_expenses": "மொத்த செலவுகள்", "net_savings": "நிகர சேமிப்பு", "predicted_next_day": "அடுத்த நாள் கணிப்பு"}
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
        u, p = st.text_input("Username"), st.text_input("Password", type="password")
        if st.button("Unlock Vault 🔑"):
            db_path = "users_database.csv"
            if os.path.exists(db_path):
                users = pd.read_csv(db_path)
                if not users[(users['username'] == u) & (users['password'] == p)].empty:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.rerun()
                else: st.error("Access Denied.")
            else: st.info("No accounts found. Please Create Account first.")
    with t_signup:
        nu, np, fn = st.text_input("New User"), st.text_input("New Pass", type="password"), st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        job = st.selectbox("Job", ["Delivery Partner", "Ride-share", "Freelancer", "Other"])
        if st.button("Create My Vault"):
            db_path = "users_database.csv"
            row = pd.DataFrame([{"username": nu, "password": np}])
            if os.path.exists(db_path):
                all_u = pd.read_csv(db_path)
                pd.concat([all_u, row]).to_csv(db_path, index=False)
            else: row.to_csv(db_path, index=False)
            pd.DataFrame([{"Name": fn, "Age": age, "Job": job}]).to_csv(get_user_profile_file(nu), index=False)
            st.success("Vault Created! Login now.")
    st.stop()

# --- 3. MAIN APP ---
USER_ID = st.session_state.username
LOCAL_SAVE_FILE = get_user_data_file(USER_ID)
if os.path.exists(get_user_profile_file(USER_ID)):
    user_bio = pd.read_csv(get_user_profile_file(USER_ID)).iloc[0]
else: user_bio = {"Name": USER_ID, "Job": "Gig Worker"}

st.set_page_config(page_title="Coach Dashboard", layout="wide")

with st.sidebar:
    st.title(f"👑 {user_bio['Name']}")
    if st.button("Exit Vault"): st.session_state.authenticated = False; st.rerun()
    st.markdown("---")
    sel_lang = st.selectbox("Language / மொழி", list(LANGUAGES.keys()))
    t = LANGUAGES[sel_lang]
    input_method = st.radio("Input Mode", ["Manual Entry", "Upload CSV"])
    uploaded_file = st.file_uploader("Upload CSV", type="csv") if input_method == "Upload CSV" else None

# Manual Entry with Calendar
if "manual_df" not in st.session_state:
    if os.path.exists(LOCAL_SAVE_FILE):
        st.session_state.manual_df = pd.read_csv(LOCAL_SAVE_FILE)
        st.session_state.manual_df['Date'] = pd.to_datetime(st.session_state.manual_df['Date'])
    else:
        st.session_state.manual_df = pd.DataFrame(columns=["Date", "Income", "Tips", "Working Hours", "Expense", "Category", "Description"])

if input_method == "Manual Entry":
    st.title("Financial Entry ✍️")
    col_config = {"Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY")}
    ed = st.data_editor(st.session_state.manual_df, column_config=col_config, num_rows="dynamic", use_container_width=True)
    if st.button(t["save_data"]): ed.to_csv(LOCAL_SAVE_FILE, index=False); st.success("Saved!")
    st.session_state.manual_df = ed

# Processing
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
        cols = st.columns(4)
        cols[0].metric(t["total_income"], f"₹{df['Income'].sum()+df['Tips'].sum():,.0f}")
        cols[1].metric(t["total_expenses"], f"₹{df['Expense'].sum():,.0f}")
        cols[2].metric(t["net_savings"], f"₹{(df['Income'].sum()+df['Tips'].sum())-df['Expense'].sum():,.0f}")
        cols[3].metric(t["predicted_next_day"], f"₹{pred:,.0f}")

        t1, t2, t3, t4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])
        with t1:
            fig = vis.plot_income_trend(daily_df, lean, thresh)
            if fig: st.plotly_chart(fig, use_container_width=True)
            st.markdown("### 🗓️ Monthly Snapshot")
            st.dataframe(ana.monthly_aggregation(df), use_container_width=True, hide_index=True)
else:
    st.info("👈 Please enter or upload data in the sidebar.")
