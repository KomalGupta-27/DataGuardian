import streamlit as st
import pandas as pd
import os
from datetime import datetime

from database.models import get_all_datasets, get_validation_results
from services.report_generator import ReportGenerator



st.title("Executive Reports")
st.caption("Generate, view, and export comprehensive corporate data quality and compliance reports.")

# Fetch datasets
datasets = get_all_datasets()

if not datasets:
    st.warning("No datasets found in SQLite. Please upload a dataset first.")
    if st.button("Go to Upload Page", type="primary"):
        st.switch_page("app_pages/Upload.py")
    st.stop()

# Format select box options
dataset_options = {
    f"{d['filename']} (ID: {d['dataset_id']} - {d['status']} - Score: {d['quality_score']}%)": d
    for d in datasets
}

selected_option = st.selectbox(
    "Select Dataset to Generate Report",
    options=list(dataset_options.keys())
)

selected_dataset = dataset_options[selected_option]
dataset_id = selected_dataset["dataset_id"]
status = selected_dataset["status"]

if status != "Validated":
    st.warning(f"This dataset has status '{status}' and has not been validated yet.")
    st.info("Validation results must be computed before generating executive reports.")
    if st.button("Go to Pipeline Monitor", type="primary"):
        st.switch_page("app_pages/Pipeline_Monitor.py")
    st.stop()

st.divider()

# Generate and render markdown report
report_markdown = ReportGenerator.generate_markdown_summary(dataset_id)
st.markdown(report_markdown)

st.divider()

st.subheader("Export & Share")

col_export1, col_export2 = st.columns(2)

with col_export1:
    # Generate CSV string
    report_csv = ReportGenerator.generate_csv_report(dataset_id)
    
    st.download_button(
        "Download Detailed Issues Report (CSV)",
        report_csv,
        file_name=f"DataGuardian_Detailed_Report_{selected_dataset['filename'].split('.')[0]}.csv",
        mime="text/csv"
    )

with col_export2:
    # Create simple metric summary text for email/txt sharing
    total_issues = len(get_validation_results(dataset_id))
    summary_text = (
        f"DataGuardian Quality Scan Report\n"
        f"===================================\n"
        f"Dataset: {selected_dataset['filename']}\n"
        f"Validation Time: {selected_dataset['validation_time']}\n"
        f"Total Rows: {selected_dataset['total_rows']}\n"
        f"Quality Score: {selected_dataset['quality_score']}%\n"
        f"Total Issues Detected: {total_issues}\n"
        f"Status: {selected_dataset['status']}\n"
    )
    st.download_button(
        "Download Executive Summary (TXT)",
        summary_text,
        file_name=f"DataGuardian_Executive_Summary_{selected_dataset['filename'].split('.')[0]}.txt",
        mime="text/plain"
    )