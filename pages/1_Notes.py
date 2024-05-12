"""pages/1_Notes.py"""

import streamlit as st

st.set_page_config(page_title="Notes", page_icon="🌍")
st.title("Notes")


def read_markdown(file):
    return file.read().decode("utf-8").splitlines()


if 'uploaded_notes' not in st.session_state:
    st.session_state['uploaded_notes'] = {}

uploaded_files = st.file_uploader("Upload Markdown Files", type=['md'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        content = read_markdown(uploaded_file)
        st.session_state.uploaded_notes[uploaded_file.name] = [line for line in content if line.strip()]

if st.session_state['uploaded_notes']:
    for file_name, content in st.session_state['uploaded_notes'].items():
        with st.expander(file_name):
            for line in content:
                st.write(line)
