# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The initial UML design is a class diagram outlining the main components of PawPal+, a pet care scheduling app. It focuses on managing pets, tasks, owners, scheduling logic, and notifications, with relationships showing how they interact (e.g., owners manage pets, tasks belong to pets).

Classes included:
- **Pet**: Holds pet details like name, species, age, preferences, and health notes. Responsibilities: Update preferences and retrieve associated schedules.
- **Task**: Represents care activities with description, duration, priority, time, and pet reference. Responsibilities: Schedule, reschedule, and check completion status.
- **Owner**: Manages owner info and their pets. Responsibilities: Add/remove pets and view schedules.
- **Scheduler**: Handles task lists and constraints. Responsibilities: Generate, optimize schedules, and check for conflicts.
- **Notification**: Manages reminders for tasks. Responsibilities: Send notifications and set reminders.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed during implementation. One key change was adopting Python dataclasses for the Pet and Task classes instead of regular classes with manual __init__ methods. This was done to reduce boilerplate code, automatically generate useful methods like __repr__ and __eq__, and improve code readability and maintainability without sacrificing functionality.

## 2. Implementation

**a. Key algorithms**

- Describe one key algorithm you implemented (e.g., sorting, filtering, conflict detection).
- How does it work? Why did you choose this approach?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes (e.g., only checking for exact time matches instead of overlapping durations).

The scheduler checks for exact time matches instead of overlapping durations to keep the logic simple and avoid complex datetime range comparisons, which could increase computational overhead for large schedules. This tradeoff prioritizes ease of implementation and readability over detecting subtle conflicts like a 30-minute task overlapping with another.
