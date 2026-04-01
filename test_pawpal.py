import pytest # type: ignore
from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_completed() changes the task's status."""
    task = Task(description="Test Task", time="2023-10-01 08:00", frequency="daily")
    assert not task.is_completed()
    task.mark_completed()
    assert task.is_completed()

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Test Pet", species="Dog", age=2, preferences=[], health_notes="Healthy")
    initial_count = len(pet.tasks)
    task = Task(description="New Task", time="2023-10-01 09:00", frequency="daily")
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1