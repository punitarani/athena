"""
Streamlit App

poetry run streamlit run app.py
"""

import asyncio
from typing import Any

import nest_asyncio
import streamlit as st


st.set_page_config(page_title="Athena", page_icon=":microscope:", layout="wide")
st.title("Athena Research Studio")
