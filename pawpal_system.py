from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta


class Owner:
    def __init__(self, name: str, contact_info: str, pets: List):
        self.name = name
        self.contact_info = contact_info
        self.pets = pets

    def add_pet(self, pet):
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        self.pets = [p for p in self.pets if p.name != pet_name]

    def view_schedule(self) -> List:
        all_tasks = []
        for pet in self.pets:
            if hasattr(pet, "get_schedule"):
                all_tasks.extend(pet.get_schedule())
        return all_tasks

    def get_all_tasks(self) -> List:
        return self.view_schedule()


@dataclass
class Pet:
    name: str
    type: str
    age: int
    breed: str
    owner: Owner


@dataclass
class Task:
    name: str
    scheduled_time: datetime
    duration: int
    priority: int
    recurrence: Optional[str] = None
    completion_status: bool = False
    pet: Optional[object] = field(default=None, repr=False)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.pets: List[Pet] = []
        self._tasks: List[Task] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def add_task(self, pet: Pet, task: Task):
        task.pet = pet
        self._tasks.append(task)

    def generate_daily_plan(self, date: datetime) -> List[Task]:
        """Return all tasks (sorted by scheduled_time) that apply to the given date."""
        plan = []
        target_date = date.date()

        for task in self._tasks:
            if task.completion_status:
                continue

            task_date = task.scheduled_time.date()

            if task.recurrence is None:
                # One-time task: only on its exact date
                if task_date == target_date:
                    plan.append(task)

            elif task.recurrence == "daily":
                # Appears on every day from its start date onward
                if task_date <= target_date:
                    adjusted = Task(
                        name=task.name,
                        scheduled_time=task.scheduled_time.replace(
                            year=date.year, month=date.month, day=date.day
                        ),
                        duration=task.duration,
                        priority=task.priority,
                        recurrence=task.recurrence,
                        pet=task.pet,
                    )
                    plan.append(adjusted)

            elif task.recurrence == "weekly":
                # Appears every 7 days from its start date
                delta = (target_date - task_date).days
                if delta >= 0 and delta % 7 == 0:
                    adjusted = Task(
                        name=task.name,
                        scheduled_time=task.scheduled_time.replace(
                            year=date.year, month=date.month, day=date.day
                        ),
                        duration=task.duration,
                        priority=task.priority,
                        recurrence=task.recurrence,
                        pet=task.pet,
                    )
                    plan.append(adjusted)

        return sorted(plan, key=lambda t: t.scheduled_time)

    def mark_complete(self, task: Task, _date: datetime):
        """Mark a task complete. For daily tasks, schedule a one-time follow-up for the next day."""
        task.completion_status = True
        if task.recurrence == "daily":
            next_time = task.scheduled_time + timedelta(days=1)
            new_task = Task(
                name=task.name,
                scheduled_time=next_time,
                duration=task.duration,
                priority=task.priority,
                recurrence=None,  # One-time continuation; no further auto-generation
                pet=task.pet,
            )
            self._tasks.append(new_task)
        # Weekly tasks: just mark done, no continuation


class Notification:
    def __init__(self, task_id: int, reminder_time: str, message: str):
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.message = message

    def send_notification(self):
        print(f"Sending notification: {self.message}")

    def set_reminder(self, time: str):
        self.reminder_time = time
