import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import data_processing as dp, categorization as cat, analysis as ana, visualization as vis, advisor as adv
import os
import datetime

# --- PRIVATE DATA ISOLATION LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

def get_user_data_file(username):
    return f"data_private_{username}.csv"

def get_user_profile_file(username):
    return f"profile_{username}.csv"

def get_users_db_file():
    return "users_database.csv"

# --- LOGIN / SIGNUP UI ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="AI Finance Coach - Login", layout="centered")
    st.markdown("<h1 style='text-align: center;'>🔐 Gig Worker Vault</h1>", unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Login", "Create Account"])
    
    with tab_login:
        login_user = st.text_input("Username", key="l_user")
        login_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Access Dashboard"):
            db = get_users_db_file()
            if os.path.exists(db):
                u_df = pd.read_csv(db)
                if not u_df[(u_df['username'] == login_user) & (u_df['password'] == login_pass)].empty:
                    st.session_state.authenticated = True
                    st.session_state.username = login_user
                    st.rerun()
                else: st.error("Wrong details.")
            else: st.error("No users found.")
                
    with tab_signup:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        fn = st.text_input("Full Name")
        if st.button("Create Account"):
            db = get_users_db_file()
            u_row = pd.DataFrame([{"username": new_u, "password": new_p}])
            if os.path.exists(db):
                all_u = pd.read_csv(db)
                all_u = pd.concat([all_u, u_row], ignore_index=True)
                all_u.to_csv(db, index=False)
            else: u_row.to_csv(db, index=False)
            pd.DataFrame([{"Name": fn, "Age": 25, "Gig": "Delivery"}]).to_csv(get_user_profile_file(new_u), index=False)
            st.success("Created! Go to Login.")
    st.stop()

# --- MAIN APP ---
USER_ID = st.session_state.username
LOCAL_SAVE_FILE = get_user_data_file(USER_ID)

if os.path.exists(get_user_profile_file(USER_ID)):
    user_bio = pd.read_csv(get_user_profile_file(USER_ID)).iloc[0]
else: user_bio = {"Name": USER_ID, "Age": 25, "Gig": "Independent"}

st.set_page_config(page_title=f"Coach | {user_bio['Name']}", layout="wide")

# Initialize Data
if "manual_df" not in st.session_state:
    if os.path.exists(LOCAL_SAVE_FILE):
        st.session_state.manual_df = pd.read_csv(LOCAL_SAVE_FILE)
        st.session_state.manual_df['Date'] = pd.to_datetime(st.session_state.manual_df['Date'])
    else:
        st.session_state.manual_df = pd.DataFrame(columns=["Date", "Income", "Tips", "Working Hours", "Expense", "Category", "Description"])

# Sidebar
with st.sidebar:
    st.title(f"👤 {user_bio['Name']}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    st.markdown("---")
    input_method = st.radio("Input Method", ["Manual Entry", "Upload CSV"])

if input_method == "Manual Entry":
    st.title("Financial Entry ✍️")
    edited_df = st.data_editor(st.session_state.manual_df, num_rows="dynamic", use_container_width=True)
    if st.button("Process & Save Data", type="primary"):
        edited_df.to_csv(LOCAL_SAVE_FILE, index=False)
        st.session_state.manual_df = edited_df
        st.rerun()

# Dashboard Logic
if not st.session_state.manual_df.empty:
    df = st.session_state.manual_df.copy()
    df = cat.apply_categorization(df)
    daily_df = ana.daily_aggregation(df)
    prediction, volatility = ana.predict_future_income(daily_df)
    lean_days, threshold = ana.detect_lean_periods(daily_df) # <--- Variable name is 'lean_days'

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income", f"₹{df['Income'].sum() + df['Tips'].sum():,.2f}")
    c2.metric("Total Expenses", f"₹{df['Expense'].sum():,.2f}")
    c3.metric("Predicted Next Day", f"₹{prediction:,.2f}")

    tab1, tab2, tab3 = st.tabs(["Trends", "Insights", "Advisor"])
    
    with tab1:
        # Calling with 'lean_days'
        fig = vis.plot_income_trend(daily_df, lean_days, threshold)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Ask AI Advisor")
        q = st.text_input("Question")
        if st.button("Ask"):
            st.success(adv.ai_financial_response(q, daily_df))



