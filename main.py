# Step 1: Study planner

subjects = input("Enter subjects (comma separated): ")
hours = int(input("Enter total study hours: "))

subject_list = subjects.split(",")
time_per_subject = hours / len(subject_list)

print("\n📅 Today's Study Plan:")
for subject in subject_list:
    print(f"- {subject.strip()} → {time_per_subject:.1f} hours")


# Step 2: Habit tracker

habits = ["Study", "Exercise", "Drink Water"]

print("\n🔥 Habit Tracker:")

completed = []

for habit in habits:
    done = input(f"Did you complete {habit}? (yes/no): ")
    if done.lower() == "yes":
        completed.append(habit)

print("\n✅ Completed Habits:")
for habit in completed:
    print("-", habit)