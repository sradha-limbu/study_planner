import tkinter as tk
from tkinter import messagebox
import json
from datetime import date, timedelta

root = tk.Tk()
root.title("Study Planner + Habit Tracker")
root.geometry("700x700")

habits = ["Study", "Exercise", "Drink Water"]
habit_vars = []

today = str(date.today())

# --------------------------
# Load history
# --------------------------
try:
    with open("data.json", "r") as file:
        old_data = json.load(file)
    if "history" in old_data:
        history = old_data["history"]
    else:
        history = {today: {"plan": old_data.get("plan", {}), "completed_habits": old_data.get("completed_habits", [])}}
except:
    history = {}

# --------------------------
# Display previous data
# --------------------------
tk.Label(root, text="Previous Day(s) Data:", font=("Arial", 12, "bold")).pack(pady=5)
if history:
    last_date = sorted(history.keys())[-1]
    last_day = history[last_date]
    tk.Label(root, text=f"Date: {last_date}", font=("Arial", 10, "italic")).pack()
    for subject, time in last_day["plan"].items():
        tk.Label(root, text=f"- {subject} → {time} hours").pack()
    tk.Label(root, text="Completed Habits:").pack()
    for habit in last_day["completed_habits"]:
        tk.Label(root, text=f"- {habit}").pack()
else:
    tk.Label(root, text="No previous data found").pack()

# --------------------------
# Input for today
# --------------------------
tk.Label(root, text="\nEnter Subjects (comma separated):").pack(pady=5)
subjects_entry = tk.Entry(root, width=50)
subjects_entry.pack(pady=5)

tk.Label(root, text="Total Study Hours:").pack(pady=5)
hours_entry = tk.Entry(root, width=50)
hours_entry.pack(pady=5)

tk.Label(root, text="\nSelect Completed Habits:").pack(pady=5)
for habit in habits:
    var = tk.IntVar()
    if today in history and habit in history[today].get("completed_habits", []):
        var.set(1)
    tk.Checkbutton(root, text=habit, variable=var).pack(anchor='w')
    habit_vars.append(var)

# --------------------------
# Function to save data
# --------------------------
def save_data():
    subjects = subjects_entry.get().split(",")
    if len(subjects) == 0 or subjects[0].strip() == "":
        messagebox.showwarning("Input Error", "Please enter at least one subject.")
        return

    try:
        hours = int(hours_entry.get())
    except:
        messagebox.showwarning("Input Error", "Please enter a valid number for hours.")
        return

    time_per_subject = hours / len(subjects)
    plan = {subject.strip(): time_per_subject for subject in subjects}
    completed = [habit for habit, var in zip(habits, habit_vars) if var.get() == 1]

    history[today] = {
        "plan": plan,
        "completed_habits": completed
    }

    with open("data.json", "w") as file:
        json.dump({"history": history}, file, indent=4)

    progress = (len(completed)/len(habits)) * 100

    # Calculate streak
    streak = 0
    sorted_dates = sorted(history.keys(), reverse=True)
    for day in sorted_dates:
        if set(history[day]["completed_habits"]) == set(habits):
            streak += 1
        else:
            break

    messagebox.showinfo("Saved!", f"Data saved!\nProgress: {progress:.1f}%\nCurrent Streak: {streak} day(s)")

    # Refresh calendar
    draw_calendar()

# --------------------------
# Calendar display
# --------------------------
calendar_frame = tk.Frame(root)
calendar_frame.pack(pady=20)

def draw_calendar():
    # Clear previous calendar
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    tk.Label(calendar_frame, text="Streak Calendar (Last 14 Days)", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=14)

    # Get last 14 days
    for i in range(14):
        day_date = date.today() - timedelta(days=13 - i)
        day_str = str(day_date)
        completed_all = day_str in history and set(history[day_str]["completed_habits"]) == set(habits)
        color = "green" if completed_all else "white"
        tk.Label(calendar_frame, text=day_date.strftime("%d"), bg=color, width=4, relief="solid").grid(row=1, column=i, padx=2, pady=2)

draw_calendar()

# --------------------------
# Save button
# --------------------------
tk.Button(root, text="Save Plan & Habits", command=save_data, bg="green", fg="white").pack(pady=20)

root.mainloop()