import tkinter as tk
from tkinter import messagebox
import json
from datetime import date, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

# --------------------------
# Main window
# --------------------------
root = tk.Tk()
root.title("Study Planner + Habit Tracker")
root.geometry("900x800")
root.configure(bg="#f0f4f7")  # soft background color

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
# Previous days frame (scrollable)
# --------------------------
prev_frame_container = tk.Frame(root, bg="#f0f4f7")
prev_frame_container.pack(pady=10, fill="both", expand=False)

prev_canvas = tk.Canvas(prev_frame_container, height=150, bg="#f0f4f7")
prev_scrollbar = tk.Scrollbar(prev_frame_container, orient="vertical", command=prev_canvas.yview)
prev_scrollable_frame = tk.Frame(prev_canvas, bg="#f0f4f7")

prev_scrollable_frame.bind(
    "<Configure>",
    lambda e: prev_canvas.configure(scrollregion=prev_canvas.bbox("all"))
)

prev_canvas.create_window((0, 0), window=prev_scrollable_frame, anchor="nw")
prev_canvas.configure(yscrollcommand=prev_scrollbar.set)

prev_canvas.pack(side="left", fill="both", expand=True)
prev_scrollbar.pack(side="right", fill="y")

def display_previous_data():
    for widget in prev_scrollable_frame.winfo_children():
        widget.destroy()

    tk.Label(prev_scrollable_frame, text="Previous Day(s) Data:", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=5)
    if history:
        for day in sorted(history.keys(), reverse=True):
            day_data = history[day]
            tk.Label(prev_scrollable_frame, text=f"Date: {day}", font=("Arial", 11, "italic"), bg="#d1e7dd", anchor='w').pack(fill='x', padx=10, pady=2)
            for subject, time_h in day_data.get("plan", {}).items():
                tk.Label(prev_scrollable_frame, text=f"- {subject} → {time_h} hours", bg="#f0f4f7").pack(anchor='w', padx=20)
            tk.Label(prev_scrollable_frame, text="Completed Habits:", font=("Arial", 10, "bold"), bg="#f0f4f7").pack(anchor='w', padx=20)
            for habit in day_data.get("completed_habits", []):
                tk.Label(prev_scrollable_frame, text=f"- {habit}", bg="#f0f4f7").pack(anchor='w', padx=40)
            tk.Label(prev_scrollable_frame, text="").pack()
    else:
        tk.Label(prev_scrollable_frame, text="No previous data found", bg="#f0f4f7").pack()

display_previous_data()

# --------------------------
# Input fields
# --------------------------
input_frame = tk.Frame(root, bg="#f0f4f7")
input_frame.pack(pady=10, fill="x")

tk.Label(input_frame, text="Enter Subjects (comma separated):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
subjects_entry = tk.Entry(input_frame, width=50, font=("Arial", 11))
subjects_entry.pack(pady=5)

tk.Label(input_frame, text="Total Study Hours:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
hours_entry = tk.Entry(input_frame, width=50, font=("Arial", 11))
hours_entry.pack(pady=5)

tk.Label(input_frame, text="Select Completed Habits:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
for habit in habits:
    var = tk.IntVar()
    if today in history and habit in history[today].get("completed_habits", []):
        var.set(1)
    tk.Checkbutton(input_frame, text=habit, variable=var, bg="#f0f4f7", font=("Arial", 11)).pack(anchor='w')
    habit_vars.append(var)

# --------------------------
# Calendar frame
# --------------------------
calendar_container = tk.Frame(root, bg="#f0f4f7")
calendar_container.pack(pady=20, fill="x")

canvas = tk.Canvas(calendar_container, height=50, bg="#f0f4f7")
scrollbar = tk.Scrollbar(calendar_container, orient="horizontal", command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg="#f0f4f7")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar.set)

canvas.pack(side="top", fill="x", expand=True)
scrollbar.pack(side="bottom", fill="x")

def draw_calendar(days=30):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    tk.Label(scrollable_frame, text="Streak Calendar (Last {} Days)".format(days), font=("Arial", 12, "bold"), bg="#f0f4f7").grid(row=0, column=0, columnspan=days)

    for i in range(days):
        day_date = date.today() - timedelta(days=days-1-i)
        day_str = str(day_date)
        completed_all = day_str in history and set(history[day_str]["completed_habits"]) == set(habits)
        if day_str == today:
            color = "orange" if not completed_all else "green"
        else:
            color = "green" if completed_all else "white"
        tk.Label(scrollable_frame, text=day_date.strftime("%d"), bg=color, width=4, relief="solid").grid(row=1, column=i, padx=2, pady=2)

draw_calendar()

# --------------------------
# Progress Bar (weekly)
# --------------------------
progress_frame = tk.Frame(root, bg="#f0f4f7")
progress_frame.pack(pady=20, fill="both", expand=True)

def draw_progress_chart():
    for widget in progress_frame.winfo_children():
        widget.destroy()

    days = sorted(history.keys(), reverse=True)[:7]
    days.reverse()
    progress_values = []
    for day in days:
        completed = len(history[day]["completed_habits"])
        progress_values.append((completed/len(habits))*100)

    fig, ax = plt.subplots(figsize=(6,2))
    ax.bar(days, progress_values, color="#4caf50")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Progress %")
    ax.set_title("Last 7 Days Progress")
    ax.set_xticklabels(days, rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    canvas_chart = FigureCanvasTkAgg(fig, master=progress_frame)
    canvas_chart.draw()
    canvas_chart.get_tk_widget().pack()

draw_progress_chart()

# --------------------------
# Save function
# --------------------------
def save_data():
    global habit_vars

    subjects = [s.strip() for s in subjects_entry.get().split(",") if s.strip() != ""]
    if len(subjects) == 0:
        messagebox.showwarning("Input Error", "Please enter at least one subject.")
        return

    try:
        hours = int(hours_entry.get())
    except:
        messagebox.showwarning("Input Error", "Please enter a valid number for hours.")
        return

    time_per_subject = hours / len(subjects)
    plan = {subject: time_per_subject for subject in subjects}

    completed = [habit for habit, var in zip(habits, habit_vars) if var.get() == 1]

    history[today] = {
        "plan": plan,
        "completed_habits": completed
    }

    with open("data.json", "w") as file:
        json.dump({"history": history}, file, indent=4)

    progress = (len(completed)/len(habits)) * 100

    streak = 0
    sorted_dates = sorted(history.keys(), reverse=True)
    for day in sorted_dates:
        if set(history[day]["completed_habits"]) == set(habits):
            streak += 1
        else:
            break

    messagebox.showinfo("Saved!", f"Data saved!\nProgress: {progress:.1f}%\nCurrent Streak: {streak} day(s)")

    draw_calendar()
    display_previous_data()
    draw_progress_chart()

# --------------------------
# Save button
# --------------------------
tk.Button(root, text="Save Plan & Habits", command=save_data, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# --------------------------
# Habit Reminders
# --------------------------
reminder_times = {
    "Study": "18:00",
    "Exercise": "19:00",
    "Drink Water": ["10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
}

def check_reminders():
    current_time = time.strftime("%H:%M")
    for habit, times in reminder_times.items():
        if isinstance(times, str):
            times = [times]
        if current_time in times:
            messagebox.showinfo("Reminder", f"⏰ Time to {habit}!")
    root.after(60000, check_reminders)

root.after(1000, check_reminders)

root.mainloop()