import streamlit as st



st.title("Settings")
st.caption("Configure DataGuardian preferences and application thresholds.")

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

st.subheader("Application Details")

st.text_input(
    "Default Upload Directory",
    value="data/uploaded",
    disabled=True
)

st.text_input(
    "Database Type",
    value="SQLite",
    disabled=True
)

st.text_input(
    "Build Version",
    value="DataGuardian v1.0.0",
    disabled=True
)

st.divider()

if st.button("Save Settings", type="primary"):
    st.success("Settings saved successfully.")