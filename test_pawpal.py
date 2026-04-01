import pytest
from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Scheduler, Owner  # Added Owner import

class TestPetScheduler:
    """Unit tests for PawPal+ pet scheduler, focusing on happy paths and edge cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.owner = Owner("John Doe", "john@example.com", [])  # Create Owner instance with contact_info and pets list
        # Assuming Pet.__init__(name, type, age, breed, owner) where owner is Owner object
        self.pet = Pet("Buddy", "Dog", 5, "Golden Retriever", self.owner)
        # Assuming Scheduler.__init__(owner) where owner is Owner object
        self.scheduler = Scheduler(self.owner)
        self.scheduler.add_pet(self.pet)

    # Happy Paths
    def test_basic_task_scheduling_and_sorting(self):
        """Test basic task creation and sorting by time."""
        task1 = Task("Feed", datetime(2023, 10, 1, 8, 0), duration=30, priority=1)
        task2 = Task("Walk", datetime(2023, 10, 1, 10, 0), duration=60, priority=2)
        self.scheduler.add_task(self.pet, task1)
        self.scheduler.add_task(self.pet, task2)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 2
        assert plan[0].name == "Feed"  # Sorted by time
        assert plan[1].name == "Walk"

    def test_multiple_pets_with_tasks(self):
        """Test scheduling and sorting across multiple pets."""
        owner2 = Owner("Jane Doe", "jane@example.com", [])  # Create second Owner
        pet2 = Pet("Whiskers", "Cat", 2, "Siamese", owner2)
        self.scheduler.add_pet(pet2)
        task1 = Task("Feed Buddy", datetime(2023, 10, 1, 8, 0), duration=30, priority=1)
        task2 = Task("Feed Whiskers", datetime(2023, 10, 1, 9, 0), duration=30, priority=1)
        self.scheduler.add_task(self.pet, task1)
        self.scheduler.add_task(pet2, task2)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 2
        assert plan[0].pet.name == "Buddy"
        assert plan[1].pet.name == "Whiskers"

    def test_recurring_tasks(self):
        """Test recurring task generation."""
        task = Task("Groom", datetime(2023, 10, 1, 14, 0), duration=45, priority=3, recurrence="daily")
        self.scheduler.add_task(self.pet, task)
        self.scheduler.mark_complete(task, datetime(2023, 10, 1))
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 2))
        assert len(plan) == 1
        assert plan[0].name == "Groom"
        assert plan[0].scheduled_time == datetime(2023, 10, 2, 14, 0)

    def test_sorting_with_priorities(self):
        """Test sorting by time (priorities ignored per README)."""
        task1 = Task("Vet", datetime(2023, 10, 1, 9, 0), duration=60, priority=1)
        task2 = Task("Play", datetime(2023, 10, 1, 9, 30), duration=30, priority=3)
        self.scheduler.add_task(self.pet, task1)
        self.scheduler.add_task(self.pet, task2)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 2
        assert plan[0].name == "Vet"  # Sorted by time, not priority

    def test_task_completion_and_updates(self):
        """Test marking tasks complete (no recurrence update assumed)."""
        task = Task("Walk", datetime(2023, 10, 1, 10, 0), duration=60, priority=2, recurrence="weekly")
        self.scheduler.add_task(self.pet, task)
        self.scheduler.mark_complete(task, datetime(2023, 10, 1))
        # No update to recurrence assumed
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 8))
        assert len(plan) == 0  # No auto-generation

    # Edge Cases
    def test_pet_with_no_tasks(self):
        """Test scheduler with a pet having no tasks."""
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 0

    def test_tasks_at_exact_same_time(self):
        """Test handling tasks at identical times (order undefined)."""
        task1 = Task("Feed", datetime(2023, 10, 1, 9, 0), duration=30, priority=1)
        task2 = Task("Meds", datetime(2023, 10, 1, 9, 0), duration=15, priority=2)
        self.scheduler.add_task(self.pet, task1)
        self.scheduler.add_task(self.pet, task2)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 2
        # No assumption on order for ties

    def test_recurring_task_overlaps(self):
        """Test recurring task with a one-time task (no conflict detection)."""
        recurring = Task("Walk", datetime(2023, 10, 1, 10, 0), duration=60, priority=2, recurrence="daily")
        one_time = Task("Vet", datetime(2023, 10, 5, 10, 0), duration=120, priority=1)
        self.scheduler.add_task(self.pet, recurring)
        self.scheduler.add_task(self.pet, one_time)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 5))
        assert len(plan) == 2  # Both present, no conflict check

    def test_recurring_task_end_date(self):
        """Test recurring task (no end_date handling)."""
        task = Task("Groom", datetime(2023, 10, 1, 14, 0), duration=45, priority=3, recurrence="weekly")
        self.scheduler.add_task(self.pet, task)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 22))
        assert len(plan) == 1  # Continues indefinitely

    def test_large_number_of_tasks(self):
        """Test sorting with many tasks."""
        for i in range(50):
            task = Task(f"Task{i}", datetime(2023, 10, 1, 8, 0) + timedelta(minutes=i), duration=30, priority=i % 3 + 1)
            self.scheduler.add_task(self.pet, task)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 50
        assert plan[0].scheduled_time < plan[1].scheduled_time

    def test_boundary_dates_times(self):
        """Test tasks near midnight and leap year."""
        task1 = Task("Midnight Feed", datetime(2023, 10, 1, 23, 59), duration=1, priority=1)
        task2 = Task("Leap Groom", datetime(2024, 2, 29, 12, 0), duration=30, priority=2)
        self.scheduler.add_task(self.pet, task1)
        self.scheduler.add_task(self.pet, task2)
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 1
        assert plan[0].name == "Midnight Feed"
        plan_leap = self.scheduler.generate_daily_plan(datetime(2024, 2, 29))
        assert len(plan_leap) == 1

    def test_empty_scheduler(self):
        """Test scheduler with no pets or tasks."""
        owner_test = Owner("Test Owner", "test@example.com", [])
        empty_scheduler = Scheduler(owner_test)
        plan = empty_scheduler.generate_daily_plan(datetime(2023, 10, 1))
        assert len(plan) == 0

    def test_recurring_task_modifications(self):
        """Test modifying recurrence (no dynamic update)."""
        task = Task("Walk", datetime(2023, 10, 1, 10, 0), duration=60, priority=2, recurrence="daily")
        self.scheduler.add_task(self.pet, task)
        self.scheduler.mark_complete(task, datetime(2023, 10, 1))
        task.recurrence = "weekly"  # No effect
        plan = self.scheduler.generate_daily_plan(datetime(2023, 10, 8))
        assert len(plan) == 0  # No auto-generation