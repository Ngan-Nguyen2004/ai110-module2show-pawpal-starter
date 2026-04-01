from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    time: str  # e.g., "2023-10-01 08:00"
    frequency: str  # e.g., "daily", "weekly"
    completion_status: bool = False

    def schedule(self, new_time: str):
        """Schedules the task to a new time."""
        self.time = new_time

    def reschedule(self, new_time: str):
        """Reschedules the task to a new time."""
        self.time = new_time

    def is_completed(self) -> bool:
        """Returns True if the task is completed."""
        return self.completion_status

    def mark_completed(self):
        """Marks the task as completed and creates a new recurring task if applicable."""
        self.completion_status = True
        if self.frequency == "daily":
            next_time = (datetime.fromisoformat(self.time) + timedelta(days=1)).isoformat()
            # Note: Need to associate with pet; for now, assume caller handles adding to pet
        elif self.frequency == "weekly":
            next_time = (datetime.fromisoformat(self.time) + timedelta(weeks=1)).isoformat()
        # In practice, return the new task or add to pet's tasks list

@dataclass
class Pet:
    name: str
    species: str
    age: int
    preferences: List[str]
    health_notes: str
    tasks: List[Task] = None

    def __post_init__(self):
        """Initializes the tasks list if None."""
        if self.tasks is None:
            self.tasks = []

    def update_preferences(self, preferences: List[str]):
        """Updates the pet's preferences."""
        self.preferences = preferences

    def get_schedule(self) -> List[Task]:
        """Returns the pet's list of tasks."""
        return self.tasks

    def add_task(self, task: Task):
        """Adds a task to the pet's schedule."""
        self.tasks.append(task)

class Owner:
    def __init__(self, name: str, contact_info: str, pets: List[Pet]):
        """Initializes the owner with name, contact info, and pets."""
        self.name = name
        self.contact_info = contact_info
        self.pets = pets

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Removes a pet from the owner's list by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def view_schedule(self):
        """Returns all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_schedule())
        return all_tasks

    def get_all_tasks(self) -> List[Task]:
        """Retrieves all tasks from all pets managed by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

class Scheduler:
    def __init__(self, owner: Owner, constraints: Dict = None):
        """Initializes the scheduler with an owner and constraints."""
        self.owner = owner
        self.constraints = constraints or {"max_daily_tasks": 10, "priority_weight": 0.5}
        self.tasks = self.owner.get_all_tasks()  # Retrieve tasks from owner's pets

    def generate_schedule(self) -> List[Task]:
        """Generates a basic schedule by sorting tasks by time."""
        return sorted(self.tasks, key=lambda t: datetime.fromisoformat(t.time))

    def optimize_schedule(self) -> List[Task]:
        """Optimizes schedule considering constraints (simplified: sort by time)."""
        # Assuming priority not in Task yet; for now, sort by time
        return self.generate_schedule()

    def check_conflicts(self) -> str:
        """Checks for time conflicts and returns a warning message."""
        times = [datetime.fromisoformat(t.time) for t in self.tasks]
        if len(times) != len(set(times)):
            return "Warning: Some tasks are scheduled at the same time!"
        return "No conflicts detected."

    def filter_tasks(self, status: str = None, pet_name: str = None) -> List[Task]:
        """Filters tasks by completion status or pet name."""
        filtered = self.tasks
        if status:
            filtered = [t for t in filtered if (status == "completed" and t.is_completed()) or (status == "pending" and not t.is_completed())]
        if pet_name:
            # Assuming we add pet_name to Task or link via pet_id; for now, skip or add later
            pass  # Placeholder: need to associate tasks with pets
        return filtered

class Notification:
    def __init__(self, task_id: int, reminder_time: str, message: str):
        """Initializes the notification with task ID, reminder time, and message."""
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.message = message

    def send_notification(self):
        """Sends the notification message."""
        print(f"Sending notification: {self.message}")

    def set_reminder(self, time: str):
        """Sets the reminder time."""
        self.reminder_time = time