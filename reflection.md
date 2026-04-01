# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design is a class diagram outlining the main components of PawPal+, a pet care scheduling app. It focuses on managing pets, tasks, owners, scheduling logic, and notifications, with relationships showing how they interact (e.g., owners manage pets, tasks belong to pets).

Classes included:
- **Pet**: Holds pet details like name, species, age, preferences, and health notes. Responsibilities: Update preferences and retrieve associated schedules.
- **Task**: Represents care activities with description, duration, priority, time, and pet reference. Responsibilities: Schedule, reschedule, and check completion status.
- **Owner**: Manages owner info and their pets. Responsibilities: Add/remove pets and view schedules.
- **Scheduler**: Handles task lists and constraints. Responsibilities: Generate, optimize schedules, and check for conflicts.
- **Notification**: Manages reminders for tasks. Responsibilities: Send notifications and set reminders.

**b. Design changes**

Yes, the design changed significantly during implementation. Key changes:

1. **Dataclasses for Pet and Task** — switched from manual `__init__` methods to Python `dataclasses` to reduce boilerplate and get `__repr__`/`__eq__` for free.
2. **Task fields renamed** — the initial `Task` used `description`, `time` (string), and `frequency`. The final version uses `name`, `scheduled_time` (datetime object), `duration`, `priority`, and `recurrence` to match test expectations and make datetime arithmetic reliable.
3. **Scheduler owns the task list** — originally, each `Pet` stored its own tasks. In the final design, `Scheduler._tasks` is the single source of truth, with each task carrying a `pet` reference. This makes `generate_daily_plan` simpler and avoids duplicating logic across pets.
4. **Pet fields simplified** — the original `Pet` had `preferences` and `health_notes`. These were replaced with `type`, `breed`, and `owner` to reflect what the UI and tests actually needed.

---

## 2. Implementation

**a. Key algorithms**

The most important algorithm is `generate_daily_plan(date)` in `Scheduler`. It works as follows:

1. Iterates over every task in `_tasks`.
2. Skips tasks with `completion_status = True`.
3. For **one-time tasks**: includes the task only if `task.scheduled_time.date() == target_date`.
4. For **daily recurring tasks**: includes the task if `task.scheduled_time.date() <= target_date`, returning a *copy* with `scheduled_time` adjusted to the target date so the original object is never mutated.
5. For **weekly recurring tasks**: includes the task if `(target_date - task_date).days % 7 == 0` and the start date is on or before the target date, again returning an adjusted copy.
6. The resulting list is sorted with `sorted(..., key=lambda t: t.scheduled_time)`.

This approach was chosen because it is stateless — it computes the plan from scratch on each call, which makes it easy to reason about and test without worrying about stale cache state.

**b. Tradeoffs**

- **Exact time match vs. overlap detection**: Conflict detection checks whether two tasks share the exact same `scheduled_time`, not whether their durations overlap. A 60-minute task at 08:00 and a 30-minute task at 08:30 would not trigger a warning, even though they overlap. This keeps the logic simple (a single dict lookup) at the cost of missing partial overlaps.
- **One-time follow-up for daily completion**: When a daily task is marked complete, the system creates a *one-time* (non-recurring) follow-up for the next day instead of a new daily task. This avoids infinite chains of recurring tasks accumulating in `_tasks`, but it means only one day of continuation is auto-generated per completion.
- **No persistent storage**: All state lives in Streamlit session state (in-memory). Refreshing the browser resets everything. A production system would need a database layer.

---

## 3. AI Strategy

**Which Copilot / AI features were most effective?**

The most effective feature was using AI for **test-driven design** — describing the expected behavior of each method in plain English and asking the AI to generate test cases, then using those tests to drive the implementation. This caught API mismatches early (e.g., the original `Task` field names didn't match what the tests expected) before any UI work began.

AI was also helpful for **boilerplate generation**: setting up the Streamlit form layouts, session state initialization, and the Mermaid UML diagram syntax, which are tedious to write by hand but follow predictable patterns.

**One example of an AI suggestion I rejected or modified**

An early AI suggestion stored recurring task state by mutating `task.scheduled_time` directly each time a plan was generated. I rejected this because it would make `generate_daily_plan` non-idempotent — calling it twice for the same date would produce different results the second time, and tests that checked `task.scheduled_time` would fail unpredictably. Instead, I kept the original task immutable and returned adjusted *copies* inside `generate_daily_plan`.

**How did using separate chat sessions for different phases help?**

Keeping separate sessions for UML design, class implementation, testing, and UI connection prevented earlier decisions from "leaking" into later prompts. For example, the UML session produced class stubs with old field names; when the testing session started fresh, it was easy to see the mismatch and fix the implementation cleanly instead of trying to patch around accumulated context.

**Lessons learned about being the "lead architect"**

The most important lesson is that AI tools are excellent *accelerators* but poor *decision-makers* for design tradeoffs. The AI could quickly generate a Scheduler class, but it took human judgment to decide that the Scheduler — not the Pet — should own the task list, because that decision had downstream consequences for testability and the UI layer. Every time I accepted an AI suggestion without understanding why, I eventually had to undo it. The cleaner workflow was: understand the tradeoff first, then let the AI write the code for the option I had already chosen.
