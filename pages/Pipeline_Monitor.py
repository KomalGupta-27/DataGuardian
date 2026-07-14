import streamlit as st
import pandas as pd
import os
import time

from utils.styles import load_css

st.set_page_config(
    page_title="Pipeline Monitor",
    layout="wide"
)

# load_css()

st.title("Pipeline Monitor")
st.caption("Monitor the execution of the data validation pipeline.")

UPLOAD_FOLDER = "data/uploaded"

files = []

if os.path.exists(UPLOAD_FOLDER):
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".csv") or f.endswith(".xlsx")
    ]

if not files:
    st.warning("No uploaded datasets available.")
    st.stop()

selected = st.selectbox(
    "Dataset",
    files
)

st.divider()

pipeline = [
    "Dataset Loaded",
    "Schema Validation",
    "Missing Value Check",
    "Duplicate Detection",
    "Business Rule Validation",
    "Quality Score Calculation",
    "Report Generation",
    "Pipeline Completed"
]

if st.button("Start Pipeline"):

    progress = st.progress(0)

    status = st.empty()

    log = st.empty()

    logs = []

    total = len(pipeline)

    for i, step in enumerate(pipeline):

        status.info(step)

        logs.append({
            "Step": step,
            "Status": "Completed"
        })

        log.dataframe(
            pd.DataFrame(logs),
            use_container_width=True,
            hide_index=True
        )

        progress.progress((i + 1) / total)

        time.sleep(0.5)

    st.success("Pipeline executed successfully.")

st.divider()

st.divider()

st.subheader("Pipeline Architecture")

st.code(
    """
Upload Dataset
      │
      ▼
Schema Validation
      │
      ▼
Data Quality Checks
      │
      ▼
Business Rule Engine
      │
      ▼
Quality Score
      │
      ▼
Report Generation
      │
      ▼
Export Results
""",
    language="text"
)

st.divider()

st.subheader("Pipeline Stages")

pipeline_status = pd.DataFrame(
    {
        "Stage": [
            "Upload",
            "Schema Validation",
            "Data Quality Checks",
            "Business Rules",
            "Quality Score",
            "Report Generation",
            "Export"
        ],
        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed"
        ]
    }
)

st.dataframe(
    pipeline_status,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption("DataGuardian v1.0 • Pipeline Monitor")