from pawpal_system import Owner, Pet, Task, Scheduler

# Create pets
pet1 = Pet(name="Fluffy", species="Cat", age=3, preferences=["morning walk"], health_notes="Healthy")
pet2 = Pet(name="Buddy", species="Dog", age=5, preferences=["evening play"], health_notes="Needs meds")

# Add tasks with different times
task1 = Task(description="Feed Fluffy", time="2023-10-01 08:00", frequency="daily")
task2 = Task(description="Walk Buddy", time="2023-10-01 09:00", frequency="daily")
task3 = Task(description="Vet check for Buddy", time="2023-10-01 10:00", frequency="weekly")

pet1.add_task(task1)
pet2.add_task(task2)
pet2.add_task(task3)

# Create owner
owner = Owner(name="John Doe", contact_info="john@example.com", pets=[pet1, pet2])

# Create scheduler and generate schedule
scheduler = Scheduler(owner)
schedule = scheduler.generate_schedule()

# Print Today's Schedule
print("Today's Schedule:")
for task in schedule:
    print(f"- {task.description} at {task.time} ({task.frequency})")