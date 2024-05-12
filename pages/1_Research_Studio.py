"""pages/1_Research_Studio.py"""

import asyncio
from typing import BinaryIO

import nest_asyncio
import streamlit as st

nest_asyncio.apply()

from athena.llm.research import run_agent

st.set_page_config(page_title="Notes", page_icon="🌍", layout="wide")
st.title("Athena Research Studio")


def read_markdown(file: BinaryIO) -> list[str]:
    """Read and decode a markdown file into a list of strings."""
    return file.read().decode("utf-8").splitlines()


def parse_prompt(_prompt: str) -> tuple[str | None, str]:
    """Extract the agent command and the remaining prompt from a given string."""
    # Handle @agent syntax:
    if _prompt.startswith("@"):
        _agent, _prompt = _prompt[1:].split(" ", 1)
        if _agent.lower() not in [
            "analyze",
            "research",
            "web",
            "wiki",
            "papers",
            "write",
        ]:
            _agent = None
    else:
        _agent = None
    return _agent.lower(), _prompt


if "uploaded_notes" not in st.session_state:
    st.session_state["uploaded_notes"] = {}

with st.sidebar:
    uploaded_files = st.file_uploader(
        "Upload Notes", type=["md"], accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            content = read_markdown(uploaded_file)
            st.session_state.uploaded_notes[uploaded_file.name] = [
                line for line in content if line.strip()
            ]

    if st.session_state["uploaded_notes"]:
        for file_name, content in st.session_state["uploaded_notes"].items():
            with st.expander(file_name):
                for line in content:
                    st.write(line)

if ["memory"] not in st.session_state:
    st.session_state["memory"] = []

if ["context"] not in st.session_state:
    st.session_state["context"] = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message_agent := message.get("agent"):
            st.markdown(f"`{message_agent}` {message.get('prompt')}")
        else:
            st.write(message.get("prompt"))

if prompt_input := st.chat_input():
    agent, prompt = parse_prompt(prompt_input)

    running_text = f"Running: {prompt}"
    if agent:
        running_text = f"`{agent}` {prompt}"
    with st.spinner(running_text):
        agent_response = asyncio.run(
            run_agent(agent, prompt, st.session_state["context"])
        )

        # Add user messages to the chat history
        if agent:
            st.session_state.messages.append(
                {"role": "user", "agent": agent, "prompt": prompt}
            )
        else:
            st.session_state.messages.append({"role": "user", "prompt": prompt})

        # Add assistant messages to the chat history
        st.session_state.messages.append(
            {"role": "assistant", "prompt": agent_response}
        )
        st.rerun()
