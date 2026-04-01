import streamlit as st
from datetime import datetime, date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ---------------------------------------------------------------------------
# Session-state bootstrap
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", "jordan@example.com", [])
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# ---------------------------------------------------------------------------
# Sidebar — owner setup
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Owner Info")
    new_name = st.text_input("Your name", value=owner.name)
    new_email = st.text_input("Your email", value=owner.contact_info)
    if st.button("Update Owner"):
        owner.name = new_name
        owner.contact_info = new_email
        st.success(f"Owner updated: {new_name}")

    st.divider()
    st.markdown("**Pets registered**")
    if scheduler.pets:
        for p in scheduler.pets:
            st.markdown(f"- {p.name} ({p.type}, {p.age} yrs)")
    else:
        st.caption("No pets yet.")

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.title("🐾 PawPal+ Pet Care Scheduler")

# ── Add Pet ──────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    c1, c2, c3, c4 = st.columns(4)
    pet_name  = c1.text_input("Name")
    pet_type  = c2.selectbox("Type", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
    pet_age   = c3.number_input("Age (yrs)", min_value=0, max_value=30, value=3)
    pet_breed = c4.text_input("Breed")
    if st.form_submit_button("Add Pet") and pet_name:
        new_pet = Pet(pet_name, pet_type, int(pet_age), pet_breed, owner)
        scheduler.add_pet(new_pet)
        owner.add_pet(new_pet)
        st.success(f"Added **{pet_name}** the {pet_type}!")

st.divider()

# ── Add Task ─────────────────────────────────────────────────────────────────
st.subheader("Schedule a Task")
if not scheduler.pets:
    st.info("Add a pet above before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_pet_name = st.selectbox("Pet", [p.name for p in scheduler.pets])
            task_name   = st.text_input("Task name", value="Morning walk")
            recurrence  = st.selectbox("Recurrence", ["None", "daily", "weekly"])
        with c2:
            task_date   = st.date_input("Date", value=date.today())
            task_time_v = st.time_input("Time", value=time(8, 0))
            duration    = st.number_input("Duration (min)", min_value=1, max_value=480, value=30)
            priority    = st.selectbox(
                "Priority",
                [1, 2, 3],
                format_func=lambda x: {1: "1 — High", 2: "2 — Medium", 3: "3 — Low"}[x],
            )
        if st.form_submit_button("Add Task") and task_name:
            pet = next(p for p in scheduler.pets if p.name == selected_pet_name)
            scheduled_dt = datetime.combine(task_date, task_time_v)
            new_task = Task(
                name=task_name,
                scheduled_time=scheduled_dt,
                duration=int(duration),
                priority=priority,
                recurrence=None if recurrence == "None" else recurrence,
            )
            scheduler.add_task(pet, new_task)
            st.success(
                f"Task **'{task_name}'** added for **{selected_pet_name}** "
                f"at {scheduled_dt.strftime('%b %d, %H:%M')} "
                f"({'one-time' if recurrence == 'None' else recurrence})."
            )

st.divider()

# ── Mark Task Complete ────────────────────────────────────────────────────────
st.subheader("Mark a Task Complete")
pending = [t for t in scheduler._tasks if not t.completion_status]
if not pending:
    st.caption("No pending tasks.")
else:
    task_labels = {
        f"{t.name} — {t.pet.name if t.pet else '?'} @ {t.scheduled_time.strftime('%b %d %H:%M')}": t
        for t in pending
    }
    chosen_label = st.selectbox("Select task to complete", list(task_labels.keys()))
    if st.button("Mark Complete"):
        chosen_task = task_labels[chosen_label]
        scheduler.mark_complete(chosen_task, datetime.today())
        if chosen_task.recurrence == "daily":
            next_dt = chosen_task.scheduled_time
            st.success(
                f"✅ **{chosen_task.name}** marked complete. "
                f"Next occurrence scheduled for {(next_dt).strftime('%b %d')}."
            )
        else:
            st.success(f"✅ **{chosen_task.name}** marked complete.")

st.divider()

# ── Daily Plan ────────────────────────────────────────────────────────────────
st.subheader("Daily Plan")
c1, c2 = st.columns([2, 1])
plan_date = c1.date_input("View plan for", value=date.today(), key="plan_date")
filter_pet = c2.selectbox(
    "Filter by pet",
    ["All pets"] + [p.name for p in scheduler.pets],
    key="filter_pet",
)

if st.button("Generate Daily Plan", type="primary"):
    plan = scheduler.generate_daily_plan(datetime.combine(plan_date, time(0, 0)))

    # Optional pet filter
    if filter_pet != "All pets":
        plan = [t for t in plan if t.pet and t.pet.name == filter_pet]

    if not plan:
        st.info(f"No tasks scheduled for **{plan_date.strftime('%B %d, %Y')}**.")
    else:
        # ── Conflict detection ────────────────────────────────────────────────
        seen_times: dict = {}
        for t in plan:
            key = t.scheduled_time
            seen_times.setdefault(key, []).append(t.name)

        conflict_times = {k: v for k, v in seen_times.items() if len(v) > 1}
        if conflict_times:
            for conflict_time, task_names in conflict_times.items():
                st.warning(
                    f"⚠️ **Schedule conflict at {conflict_time.strftime('%H:%M')}:** "
                    f"{' and '.join(task_names)} are both scheduled at the same time. "
                    f"Consider moving one of them to avoid overlap."
                )
        else:
            st.success(
                f"✅ No conflicts — **{len(plan)} task(s)** sorted and ready "
                f"for {plan_date.strftime('%B %d, %Y')}."
            )

        # ── Sorted schedule table ─────────────────────────────────────────────
        priority_label = {1: "🔴 High", 2: "🟡 Medium", 3: "🟢 Low"}
        plan_rows = [
            {
                "Time": t.scheduled_time.strftime("%H:%M"),
                "Pet": t.pet.name if t.pet else "—",
                "Task": t.name,
                "Duration": f"{t.duration} min",
                "Priority": priority_label.get(t.priority, str(t.priority)),
                "Recurrence": t.recurrence.capitalize() if t.recurrence else "One-time",
            }
            for t in plan
        ]
        st.table(plan_rows)
