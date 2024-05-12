"""pages/2_Research_Agent.py"""

import asyncio
from typing import Any

import nest_asyncio
import streamlit as st

nest_asyncio.apply()

from athena.llm.research import breakdown_objective, research_planner, run_agent

st.set_page_config(page_title="Agent", layout="wide")

# Sidebar for uploading starting context
uploaded_context = st.sidebar.file_uploader("Upload Context", type=['md'])
if uploaded_context is not None:
    starting_context = uploaded_context.read().decode("utf-8").splitlines()
else:
    starting_context = []

def run_async(async_func, *args) -> Any:
    """
    Run an asynchronous function using the existing event loop.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Use a nest_asyncio applied loop to run async tasks in a running loop
        return asyncio.ensure_future(async_func(*args))
    else:
        return loop.run_until_complete(async_func(*args))


def format_steps(idea_steps: list[str]) -> str:
    """Format the objective steps."""
    formatted_steps = []
    for _idx, _step in enumerate(idea_steps):
        formatted_step = f"**{_idx + 1}**: {_step}"
        formatted_steps.append(formatted_step)
    return "\n\n".join(formatted_steps)


def format_plan(plan: list[dict]) -> str:
    """Format the strp plan."""
    formatted_plan = []
    for idx, task in enumerate(plan):
        formatted_task = f"`{task['agent']}` {task['task']}"
        formatted_plan.append(formatted_task)
    return "\n\n".join(formatted_plan)


def run_step(
        tasks: list[dict[str, str]],
        context: list[str],
        content: st.empty(),
) -> dict[str, str]:
    """Run the step."""
    log = []

    with content.container():
        for idx, task in enumerate(tasks):
            agent, task = task["agent"], task["task"]
            with st.spinner(f"Running task {idx + 1}..."):
                response = run_async(run_agent, agent, task, context)
                log.append({"agent": agent, "task": task, "response": response})

                st.write(f"`{agent}`\n**{task}**\n\n{response}\n\n")
                st.divider()

                if response:
                    context += response + "\n"

    # Return the last non-empty response from the log
    for entry in reversed(log):
        if entry["agent"] != "planner":
            return entry


if __name__ == "__main__":
    research_objective = st.text_input(
        "Research Objective",
        "Develop an experiment to test the longevity of C elegans under different environmental conditions.",
    )
    start_button = st.button(
        "Start Research",
        help="Start the research process.",
        use_container_width=True,
        disabled=("steps" in st.session_state),
    )

    st.divider()
    idea_1_col, idea_2_col, idea_3_col = st.columns(3)

    if start_button or "steps" in st.session_state:
        with st.spinner("Analyzing the objective..."):
            if "steps" not in st.session_state:
                steps = run_async(breakdown_objective, research_objective)
                st.session_state["steps"] = steps
            else:
                steps = st.session_state["steps"]

        if steps:
            st.subheader("Research Steps")
            st.write(format_steps(steps))
            run_button = st.button(
                "Run Plan", help="Run the research plan.", use_container_width=True
            )
            # TODO: allow user to to edit steps

            if run_button:
                run_context = []
                for s_id, step in enumerate(steps):
                    with st.status(f"Step {s_id + 1}: {step}"):
                        with st.spinner(f"Generating plan for step {s_id + 1}..."):
                            research_plan = run_async(research_planner, step)
                            st.write(format_plan(research_plan))
                            st.divider()

                        # Run the step
                        section_content = st.empty()
                        step_response = run_step(
                            research_plan, research_objective, section_content
                        )
                        run_context.append(f"**{step}**\n\n{step_response['response']}")
