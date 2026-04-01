import tkinter as tk
from tkinter import messagebox
import json

# Create main window
root = tk.Tk()
root.title("Study Planner + Habit Tracker")
root.geometry("600x600")

# Step 0: Habit list and variables
habits = ["Study", "Exercise", "Drink Water"]
habit_vars = []

# Load previous data
try:
    with open("data.json", "r") as file:
        old_data = json.load(file)
    previous_plan = old_data.get("plan", {})
    previous_completed = old_data.get("completed_habits", [])
except:
    previous_plan = {}
    previous_completed = []

# Step 1: Show previous data
tk.Label(root, text="Previous Study Plan:").pack(pady=5)
if previous_plan:
    for subject, time in previous_plan.items():
        tk.Label(root, text=f"- {subject} → {time} hours").pack()
else:
    tk.Label(root, text="No previous study plan found").pack()

tk.Label(root, text="\nPrevious Completed Habits:").pack(pady=5)
if previous_completed:
    for habit in previous_completed:
        tk.Label(root, text=f"- {habit}").pack()
else:
    tk.Label(root, text="No habits completed previously").pack()

# Step 2: Input for today
tk.Label(root, text="\nEnter Subjects (comma separated):").pack(pady=5)
subjects_entry = tk.Entry(root, width=50)
subjects_entry.pack(pady=5)

tk.Label(root, text="Total Study Hours:").pack(pady=5)
hours_entry = tk.Entry(root, width=50)
hours_entry.pack(pady=5)

# Step 3: Habit tracker checkboxes
tk.Label(root, text="\nSelect Completed Habits:").pack(pady=5)
for habit in habits:
    var = tk.IntVar()
    # If habit was completed previously, check it by default
    if habit in previous_completed:
        var.set(1)
    tk.Checkbutton(root, text=habit, variable=var).pack(anchor='w')
    habit_vars.append(var)

# Step 4: Function to save today's plan and habits
def save_data():
    subjects = subjects_entry.get().split(",")
    hours = int(hours_entry.get())
    time_per_subject = hours / len(subjects)

    plan = {subject.strip(): time_per_subject for subject in subjects}
    completed = [habit for habit, var in zip(habits, habit_vars) if var.get() == 1]

    data = {
        "plan": plan,
        "completed_habits": completed
    }

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    progress = (len(completed)/len(habits)) * 100
    messagebox.showinfo("Saved!", f"Data saved!\nProgress: {progress:.1f}%")

# Step 5: Save button
tk.Button(root, text="Save Plan & Habits", command=save_data).pack(pady=20)

# Run the GUI
root.mainloop()
