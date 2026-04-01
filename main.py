import json

# Step 0: Define habits and completed list
habits = ["Study", "Exercise", "Drink Water"]
completed = []

# Step 1: Load previous data
try:
    with open("data.json", "r") as file:
        old_data = json.load(file)

    print("\n📂 Previous Data Found:")

    print("\n📅 Last Study Plan:")
    for subject, time in old_data["plan"].items():
        print(f"- {subject} → {time} hours")

    print("\n🔥 Completed Habits:")
    for habit in old_data["completed_habits"]:
        print("-", habit)

except:
    print("\n(No previous data found)")

# Step 2: Study planner
subjects = input("\nEnter subjects (comma separated): ")
hours = int(input("Enter total study hours: "))

subject_list = subjects.split(",")
time_per_subject = hours / len(subject_list)

print("\n📅 Today's Study Plan:")
plan = {}

for subject in subject_list:
    subject = subject.strip()
    plan[subject] = time_per_subject
    print(f"- {subject} → {time_per_subject:.1f} hours")

# Step 3: Habit tracker
print("\n🔥 Habit Tracker:")

for habit in habits:
    done = input(f"Did you complete {habit}? (yes/no): ")
    if done.lower() == "yes":
        completed.append(habit)

print("\n✅ Completed Habits:")
for habit in completed:
    print("-", habit)

# Step 4: Save data to JSON
data = {
    "plan": plan,
    "completed_habits": completed
}

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

print("\n💾 Data saved successfully!")

# Step 5: Show progress
total = len(habits)
done = len(completed)
percentage = (done / total) * 100

print(f"\n📊 Progress: {percentage:.1f}% completed")