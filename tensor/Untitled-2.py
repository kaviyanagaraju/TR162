days = int(input("Enter number of working days: "))

total_income = 0
total_expense = 0

for i in range(1, days + 1):
    print(f"\nDay {i}")

    income = float(input("Enter income (₹): "))
    tips = float(input("Enter tips (₹): "))
    fuel = float(input("Enter fuel expense (₹): "))
    hours = int(input("Enter working hours: "))

    total_income += (income + tips)
    total_expense += fuel

    if hours > 10:
        print("⚠ Warning: You are overworking! Take rest.")

savings = total_income - total_expense

print("\n----- SUMMARY -----")
print(f"Total Income: ₹{total_income:.2f}")
print(f"Total Expense: ₹{total_expense:.2f}")
print(f"Savings: ₹{savings:.2f}")

if savings < 0:
    print("⚠ You are in loss! Reduce expenses.")
else:
    print("✅ Good job! Try saving 20% of income.")
    