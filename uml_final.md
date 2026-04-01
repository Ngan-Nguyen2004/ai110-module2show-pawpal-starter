# PawPal+ Final UML Class Diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +str contact_info
        +List~Pet~ pets
        +add_pet(pet: Pet)
        +remove_pet(pet_name: str)
        +view_schedule() List~Task~
        +get_all_tasks() List~Task~
    }

    class Pet {
        +str name
        +str type
        +int age
        +str breed
        +Owner owner
    }

    class Task {
        +str name
        +datetime scheduled_time
        +int duration
        +int priority
        +Optional~str~ recurrence
        +bool completion_status
        +Optional~Pet~ pet
    }

    class Scheduler {
        +Owner owner
        +List~Pet~ pets
        -List~Task~ _tasks
        +add_pet(pet: Pet)
        +add_task(pet: Pet, task: Task)
        +generate_daily_plan(date: datetime) List~Task~
        +mark_complete(task: Task, date: datetime)
    }

    class Notification {
        +int task_id
        +str reminder_time
        +str message
        +send_notification()
        +set_reminder(time: str)
    }

    Owner "1" --> "0..*" Pet : owns
    Pet --> Owner : belongs to
    Task --> "0..1" Pet : assigned to
    Scheduler --> Owner : manages for
    Scheduler "1" o-- "0..*" Task : tracks
    Scheduler "1" --> "0..*" Pet : schedules for
```

## Key design notes

- `Pet` and `Task` are Python **dataclasses** — fields, `__repr__`, and `__eq__` are auto-generated.
- `Task.pet` is set by `Scheduler.add_task()`, not at construction time, keeping Task creation clean.
- `Scheduler` is the single source of truth for the task list (`_tasks`). Pets no longer store their own tasks.
- `mark_complete` on a **daily** task appends a one-time follow-up for the next day; **weekly** tasks are simply closed out.
- `generate_daily_plan` returns *copies* of recurring task objects with `scheduled_time` adjusted to the requested date, so the original task objects are never mutated by the plan view.
