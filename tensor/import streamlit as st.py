import streamlit as st

st.title("Personal Finance Coach for Gig Workers")

# User details
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=100, step=1)
gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])

days = st.number_input("Enter number of working days", min_value=1, step=1)

total_income = 0.0
total_expense = 0.0

# Daily income details
for i in range(int(days)):
    st.subheader(f"Day {i+1}")

    income = st.number_input(
        f"Enter income for Day {i+1} (₹)",
        min_value=0.0,
        key=f"income_{i}"
    )

    tips = st.number_input(
        f"Enter tips for Day {i+1} (₹)",
        min_value=0.0,
        key=f"tips_{i}"
    )

    fuel = st.number_input(
        f"Enter fuel expense for Day {i+1} (₹)",
        min_value=0.0,
        key=f"fuel_{i}"
    )

    hours = st.number_input(
        f"Enter working hours for Day {i+1}",
        min_value=0,
        step=1,
        key=f"hours_{i}"
    )

    total_income += income + tips
    total_expense += fuel

    if hours > 10:
        st.warning("Warning: You are overworking. Take rest.")

# Show result button
if st.button("Calculate Summary"):
    savings = total_income - total_expense

    st.subheader("User Summary")
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Gender: {gender}")
    st.write(f"Total Income: ₹{total_income:.2f}")
    st.write(f"Total Expense: ₹{total_expense:.2f}")
    st.write(f"Savings: ₹{savings:.2f}")

    if savings < 0:
        st.error("You are in loss. Reduce expenses.")
    else:
        st.success("Good job. Try saving 20% of income.")