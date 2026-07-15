import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

from database.models import get_all_datasets, get_pipeline_logs, insert_pipeline_log
from services.pipeline import PipelineExecutor

st.title("Pipeline Monitor")
st.caption("Monitor and execute the enterprise validation pipeline on datasets.")

datasets = get_all_datasets()

if not datasets:
    st.warning("No datasets found in database. Please upload a dataset first.")
    if st.button("Go to Upload Page", type="primary"):
        st.switch_page("app_pages/Upload.py")
    st.stop()

# Selectbox options
dataset_options = {
    f"{d['filename']} (ID: {d['dataset_id']} - status: {d['status']})": d
    for d in datasets
}

selected_option = st.selectbox(
    "Select Dataset for Validation",
    options=list(dataset_options.keys())
)

selected_dataset = dataset_options[selected_option]
dataset_id = selected_dataset["dataset_id"]

# Reset run state when dataset changes
if st.session_state.get("pipeline_dataset_id") != dataset_id:
    st.session_state["pipeline_ran"] = False
    st.session_state["pipeline_success"] = False
    st.session_state["pipeline_message"] = ""
    st.session_state["pipeline_dataset_id"] = dataset_id

st.divider()

# List of steps to monitor
pipeline_steps = [
    "Dataset Loaded",
    "Schema Validation",
    "Missing Value Check",
    "Duplicate Detection",
    "Business Rule Validation",
    "Anomaly Detection",
    "Quality Score Calculation",
    "Report Generation",
    "Pipeline Completed"
]

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Execute Pipeline Run")

    if st.button("Start Pipeline Run", type="primary"):
        # Reset state for new run
        st.session_state["pipeline_ran"] = False
        st.session_state["pipeline_success"] = False

        progress_bar = st.progress(0)
        status_info = st.empty()
        log_table_placeholder = st.empty()

        logs = []
        for step in pipeline_steps:
            logs.append({"Pipeline Step": step, "Status": "Pending", "Timestamp": "-"})

        def update_log_view():
            log_table_placeholder.dataframe(
                pd.DataFrame(logs),
                width="stretch",
                hide_index=True
            )

        update_log_view()

        # Real-time callback — updates the live step log table on every stage transition
        def pipeline_callback(step, status):
            timestamp = datetime.now().strftime("%H:%M:%S")
            for log in logs:
                if log["Pipeline Step"] == step:
                    log["Status"] = status
                    log["Timestamp"] = timestamp
                    break

            try:
                step_idx = pipeline_steps.index(step)
                progress_val = (step_idx + 1) / len(pipeline_steps)
                progress_bar.progress(progress_val)
            except ValueError:
                pass

            status_info.info(f"Running: {step} — {status}")
            update_log_view()
            time.sleep(0.3)

        # Execute the actual pipeline (loads file from disk, runs all checks, stores results)
        success, message = PipelineExecutor.execute(dataset_id, callback=pipeline_callback)

        # Persist result in session state so buttons survive re-render
        st.session_state["pipeline_ran"] = True
        st.session_state["pipeline_success"] = success
        st.session_state["pipeline_message"] = message
        st.session_state["pipeline_dataset_id"] = dataset_id

        if success:
            progress_bar.progress(1.0)
            status_info.success("Validation pipeline completed. Quality scores updated in database.")
        else:
            status_info.error(f"Pipeline failed: {message}")

    # Show result buttons persistently after a successful run using session state
    if st.session_state.get("pipeline_ran") and st.session_state.get("pipeline_success"):
        st.success("Pipeline run completed successfully. Navigate to results:")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            if st.button("View Validation Metrics", width="stretch"):
                st.switch_page("app_pages/Validation.py")
        with c_res2:
            if st.button("Generate Quality Report", width="stretch"):
                st.switch_page("app_pages/Reports.py")

    elif st.session_state.get("pipeline_ran") and not st.session_state.get("pipeline_success"):
        st.error(f"Pipeline failed: {st.session_state.get('pipeline_message', 'Unknown error')}")

with right_col:
    st.subheader("Execution History Logs")

    db_logs = get_pipeline_logs(dataset_id)
    if not db_logs:
        st.info("No previous pipeline execution logs found for this dataset.")
    else:
        logs_df = pd.DataFrame(db_logs)
        display_logs = logs_df[["step", "status", "timestamp"]].copy()
        display_logs.columns = ["Step", "Status", "Timestamp"]
        st.dataframe(
            display_logs,
            width="stretch",
            hide_index=True
        )

st.divider()

st.subheader("Pipeline Stage Specifications")
st.markdown("""
* **Dataset Loaded**: Validates physical file existence and loads it into a Pandas DataFrame.
* **Schema Validation**: Evaluates structural type conformance and column indices.
* **Missing Value Check**: Scans every column and records exact row numbers with null values.
* **Duplicate Detection**: Identifies and flags fully duplicate rows.
* **Business Rule Validation**: Evaluates configured field constraints against active rules.
* **Anomaly Detection**: Flags statistical outliers (IQR method) and rapid-fire transaction velocity anomalies.
* **Quality Score Calculation**: Computes aggregate quality metric (0–100) using weighted penalties.
* **Report Generation**: Writes validation metrics and quality scores to the database.
""")