import tkinter as tk
from tkinter import messagebox

# Global variables
total_income = 0
total_expense = 0
current_day = 1

def submit_day():
    global total_income, total_expense, current_day

    try:
        income = float(income_entry.get())
        tips = float(tips_entry.get())
        fuel = float(fuel_entry.get())
        hours = int(hours_entry.get())

        total_income += (income + tips)
        total_expense += fuel

        if hours > 10:
            messagebox.showwarning("Warning", "⚠ You are overworking! Take rest.")

        current_day += 1

        if current_day > int(days_entry.get()):
            show_summary()
        else:
            day_label.config(text=f"Day {current_day}")
            clear_fields()

    except:
        messagebox.showerror("Error", "Please enter valid values")

def clear_fields():
    income_entry.delete(0, tk.END)
    tips_entry.delete(0, tk.END)
    fuel_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)

def start_tracking():
    global current_day, total_income, total_expense

    try:
        days = int(days_entry.get())
        if days <= 0:
            raise ValueError

        current_day = 1
        total_income = 0
        total_expense = 0

        setup_frame.pack_forget()
        input_frame.pack()

        day_label.config(text="Day 1")

    except:
        messagebox.showerror("Error", "Enter valid number of days")

def show_summary():
    savings = total_income - total_expense

    result = f"Total Income: ₹{total_income:.2f}\n"
    result += f"Total Expense: ₹{total_expense:.2f}\n"
    result += f"Savings: ₹{savings:.2f}\n\n"

    if savings < 0:
        result += "⚠ You are in loss! Reduce expenses."
    else:
        result += "✅ Good job! Try saving 20% of income."

    messagebox.showinfo("Summary", result)
    root.quit()

# Main Window
root = tk.Tk()
root.title("AI Finance Coach")
root.geometry("400x400")

# -------- Setup Frame --------
setup_frame = tk.Frame(root)
setup_frame.pack(pady=50)

tk.Label(setup_frame, text="Enter Working Days").pack()
days_entry = tk.Entry(setup_frame)
days_entry.pack(pady=10)

tk.Button(setup_frame, text="Start", command=start_tracking).pack()

# -------- Input Frame --------
input_frame = tk.Frame(root)

day_label = tk.Label(input_frame, text="Day 1", font=("Arial", 14))
day_label.pack(pady=10)

tk.Label(input_frame, text="Income (₹)").pack()
income_entry = tk.Entry(input_frame)
income_entry.pack()

tk.Label(input_frame, text="Tips (₹)").pack()
tips_entry = tk.Entry(input_frame)
tips_entry.pack()

tk.Label(input_frame, text="Fuel Expense (₹)").pack()
fuel_entry = tk.Entry(input_frame)
fuel_entry.pack()

tk.Label(input_frame, text="Working Hours").pack()
hours_entry = tk.Entry(input_frame)
hours_entry.pack()

tk.Button(input_frame, text="Submit Day", command=submit_day).pack(pady=20)

# Run App
root.mainloop()