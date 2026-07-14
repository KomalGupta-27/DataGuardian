import streamlit as st
from utils.styles import load_css

st.set_page_config(
    page_title="Settings",
    layout="wide"
)

# load_css()

st.title("Settings")
st.caption("Configure DataGuardian preferences.")

st.divider()

st.subheader("Validation Settings")

missing_threshold = st.slider(
    "Maximum Missing Values (%)",
    0,
    100,
    10
)

duplicate_threshold = st.slider(
    "Maximum Duplicate Rows (%)",
    0,
    100,
    5
)

negative_threshold = st.slider(
    "Maximum Negative Values (%)",
    0,
    100,
    2
)

st.divider()

st.subheader("Report Settings")

export_format = st.selectbox(
    "Default Export Format",
    [
        "CSV",
        "Excel",
        "PDF"
    ]
)

include_summary = st.checkbox(
    "Include Executive Summary",
    value=True
)

include_charts = st.checkbox(
    "Include Charts",
    value=True
)

st.divider()

st.subheader("Application")

st.text_input(
    "Default Upload Directory",
    value="data/uploaded",
    disabled=True
)

st.text_input(
    "Database",
    value="SQLite",
    disabled=True
)

st.text_input(
    "Version",
    value="DataGuardian v1.0",
    disabled=True
)

st.divider()

if st.button("Save Settings"):
    st.success("Settings saved successfully.")