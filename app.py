# app.py
import streamlit as st
from ollama import chat
from datetime import datetime

st.set_page_config(page_title="Daily Task Planner", page_icon="🗓️", layout="centered")
st.title("Daily Task Planner")

SYSTEM_PROMPT = (
    "You are a practical day-planning assistant.\n"
    "Goal: turn the user's task list into a realistic schedule.\n\n"
    "Rules:\n"
    "- Every task must have a proposed start and end time (time window).\n"
    "- Insert meal breaks: Lunch (>= 30 minutes) and Dinner (>= 30 minutes).\n"
    "- Add short buffers between blocks when helpful.\n"
    "- If task durations are missing, make reasonable estimates and keep them conservative.\n"
    "- If the time window is too tight, schedule the most important tasks first and defer the rest.\n"
    "- Keep output concise and easy to follow.\n\n"
    "Output format:\n"
    "- A single schedule list with lines like: 'HH:MM–HH:MM  Task'.\n"
    "- If anything is deferred, add a short 'Deferred' list at the end.\n"
)

def default_time_str_now():
    return datetime.now().strftime("%H:%M")

def normalize_time_str(t: str) -> str:
    # Basic cleanup to reduce user input issues (still let the model handle edge cases)
    return t.strip()

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Model", value="deepseek-r1:1.5b")

    include_time_window = st.checkbox("Use time window", value=True)

    # Default start time is current time (editable)
    start_time_default = default_time_str_now()
    start_time = st.text_input("Start time", value=start_time_default)

    # Reasonable default end time; user can change
    end_time = st.text_input("End time", value="18:00")

tasks = st.text_area(
    "Type your tasks (one per line or paste a list):",
    height=180,
    placeholder="- Finish stats assignment (2h)\n- Grocery shopping\n- Gym (45m)\n- Answer emails",
)

extra = st.text_area(
    "Optional context (deadlines, priorities, constraints):",
    height=90,
    placeholder="e.g., meeting 14:00–15:00, gym after 17:00, groceries before dinner",
)

col1, col2 = st.columns([1, 1])
plan_btn = col1.button("Create plan", type="primary", use_container_width=True)
clear_btn = col2.button("Clear", use_container_width=True)

if clear_btn:
    st.session_state.pop("result", None)
    st.rerun()

if plan_btn:
    if not tasks.strip():
        st.warning("Please enter at least one task.")
    else:
        user_content_parts = []
        user_content_parts.append("Tasks:")
        user_content_parts.append(tasks.strip())

        if extra.strip():
            user_content_parts.append("\nContext / constraints:")
            user_content_parts.append(extra.strip())

        if include_time_window:
            user_content_parts.append(
                f"\nAvailable time window: {normalize_time_str(start_time)}–{normalize_time_str(end_time)}"
            )

        # Explicitly remind about meals (even though system prompt already enforces it)
        user_content_parts.append("\nAlso include lunch and dinner (at least 30 minutes each).")

        user_content = "\n".join(user_content_parts)

        with st.spinner("Generating your plan..."):
            try:
                resp = chat(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_content},
                    ],
                )
                st.session_state["result"] = resp["message"]["content"]
            except Exception as e:
                st.error(f"Model call failed: {e}")

if "result" in st.session_state:
    st.subheader("Your plan")
    st.write(st.session_state["result"])