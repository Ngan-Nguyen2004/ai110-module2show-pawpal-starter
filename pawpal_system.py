from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Pet:
    name: str
    species: str
    age: int
    preferences: List[str]
    health_notes: str

    def update_preferences(self, preferences: List[str]):
        pass

    def get_schedule(self):
        pass

@dataclass
class Task:
    description: str
    duration: int
    priority: int
    required_time: str  # Assuming datetime as string for simplicity
    pet_id: int

    def schedule(self, time: str):
        pass

    def reschedule(self, new_time: str):
        pass

    def is_completed(self) -> bool:
        pass

class Owner:
    def __init__(self, name: str, contact_info: str, pets: List[Pet]):
        self.name = name
        self.contact_info = contact_info
        self.pets = pets

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, pet_id: int):
        pass

    def view_schedule(self):
        pass

class Scheduler:
    def __init__(self, tasks: List[Task], constraints: Dict):
        self.tasks = tasks
        self.constraints = constraints

    def generate_schedule(self):
        pass

    def optimize_schedule(self):
        pass

    def check_conflicts(self) -> bool:
        pass

class Notification:
    def __init__(self, task_id: int, reminder_time: str, message: str):
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.message = message

    def send_notification(self):
        pass

    def set_reminder(self, time: str):
        pass