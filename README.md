# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

| Feature | Description |
|---|---|
| **Multi-pet support** | Register multiple pets under one owner; each task is linked to a specific pet |
| **Sorting by time** | `generate_daily_plan()` returns tasks sorted by `scheduled_time` using Python's `sorted()` with a `lambda` key |
| **Conflict detection** | The UI flags any two tasks that share the exact same scheduled time with a `st.warning` message naming both tasks |
| **Daily recurrence** | Completing a daily task auto-schedules a one-time follow-up for the next day via `timedelta(days=1)` |
| **Weekly recurrence** | A weekly task appears in the plan on every 7-day multiple from its start date; marking complete stops future generation |
| **Pet-level filtering** | The daily plan view lets the owner filter results to a single pet |
| **Priority labels** | Tasks carry a 1–3 priority value displayed as High / Medium / Low with colour indicators |

## 📸 Demo

<!-- After running the app, take a screenshot and save it to your project folder, then update the path below -->
<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank">
  <img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' />
</a>

> To run the app locally: `streamlit run app.py`

## Testing PawPal+

### Run the test suite

```bash
python -m pytest test_pawpal.py -v
```

### What the tests cover

The test suite contains **13 automated tests** across two categories:

**Happy paths**
- Basic task scheduling and sorting by time
- Scheduling tasks across multiple pets
- Recurring task generation (daily recurrence creates a follow-up after completion)
- Sorting tasks with different priorities (time-based ordering)
- Task completion and status updates

**Edge cases**
- Pet with no tasks (empty plan)
- Two tasks scheduled at the exact same time
- Recurring task overlapping with a one-time task (no false conflict blocking)
- Weekly recurring task continues indefinitely until marked complete
- 50 tasks sorted correctly in a large plan
- Tasks at boundary datetimes (near midnight, leap year date)
- Empty scheduler with no pets or tasks
- Modifying recurrence after completion has no unintended side effects

### Confidence Level

**4 / 5 stars**

All 13 tests pass. The core scheduling behaviors — sorting, filtering, recurring tasks, and completion logic — are well covered. One star is withheld because the Streamlit UI layer (`app.py`) is not yet integration-tested, and conflict detection (same-time tasks) is detected but not enforced.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
