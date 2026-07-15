import streamlit as st
import pandas as pd
import plotly.express as px
import os
from database.models import get_all_datasets, get_validation_results


st.title("Validation Center")
st.caption("Analyze validation and risk intelligence results stored in the database.")

# Fetch datasets from database
datasets = get_all_datasets()

if not datasets:
    st.warning("No datasets found in the system. Please upload a dataset first.")
    if st.button("Go to Upload Page", type="primary"):
        st.switch_page("app_pages/Upload.py")
    st.stop()

# Format select box options
dataset_options = {
    f"{d['filename']} (ID: {d['dataset_id']} - {d['status']} - Score: {d['quality_score']}%)": d
    for d in datasets
}

selected_option = st.selectbox(
    "Select Dataset to View Results",
    options=list(dataset_options.keys())
)

selected_dataset = dataset_options[selected_option]
dataset_id = selected_dataset["dataset_id"]
status = selected_dataset["status"]

if status != "Validated":
    st.warning(f"This dataset has status '{status}' and has not been validated yet.")
    st.info("To run the quality and risk validation pipeline, go to the Pipeline Monitor.")
    if st.button("Go to Pipeline Monitor", type="primary"):
        st.switch_page("app_pages/Pipeline_Monitor.py")
    st.stop()

# Retrieve results from database
results = get_validation_results(dataset_id)

# Compute issue summary counts
missing = sum(1 for r in results if r["issue_type"] == "Missing Value")
duplicates = sum(1 for r in results if r["issue_type"] == "Duplicate Row")
negatives = sum(1 for r in results if r["issue_type"] == "Negative Value Violation")
business = sum(1 for r in results if r["issue_type"].startswith("Business Rule:"))
anomalies = sum(1 for r in results if r["issue_type"] in ["Statistical Outlier", "Velocity Check Failure"])

total_issues = len(results)
quality = selected_dataset["quality_score"]

# -----------------------
# KPI Cards
# -----------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Quality Score", f"{quality}%")
c2.metric("Missing Values", missing)
c3.metric("Duplicate Rows", duplicates)
c4.metric("Risk & Rule Failures", business + anomalies + negatives)

st.divider()

# -----------------------
# Charts
# -----------------------
if total_issues > 0:
    left, right = st.columns(2)

    with left:
        chart_data = pd.DataFrame({
            "Issue Category": ["Missing", "Duplicates", "Negative Values", "Business Rules", "Anomalies"],
            "Count": [missing, duplicates, negatives, business, anomalies]
        })
        # Filter categories with 0 issues to make chart clean
        chart_data = chart_data[chart_data["Count"] > 0]
        
        if not chart_data.empty:
            fig = px.bar(
                chart_data,
                x="Issue Category",
                y="Count",
                color="Issue Category",
                text="Count",
                color_discrete_sequence=["#2563eb", "#475569", "#0d9488", "#b91c1c", "#d97706"]
            )
            fig.update_layout(
                height=380, 
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Geist, Inter, sans-serif"),
                xaxis=dict(gridcolor="rgba(128,128,128,0.1)"),
                yaxis=dict(gridcolor="rgba(128,128,128,0.1)")
            )
            st.subheader("Validation Issues by Category")
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No categorical issues to display.")

    with right:
        if not chart_data.empty:
            pie = px.pie(
                chart_data,
                names="Issue Category",
                values="Count",
                hole=.55,
                color_discrete_sequence=["#2563eb", "#475569", "#0d9488", "#b91c1c", "#d97706"]
            )
            pie.update_layout(
                height=380,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Geist, Inter, sans-serif")
            )
            st.subheader("Issue Distribution")
            st.plotly_chart(pie, width="stretch")

    st.divider()

# -----------------------
# Detailed Log
# -----------------------
st.subheader("Detailed Issues Log")

if not results:
    st.success("No validation issues found. The dataset passed all checks.")
else:
    results_df = pd.DataFrame(results)
    # Tidy columns
    display_df = results_df[["row_number", "column_name", "issue_type", "severity", "description"]].copy()
    display_df.columns = ["Row", "Column", "Issue Type", "Severity", "Description"]
    
    # Filter by severity
    severity_filter = st.multiselect(
        "Filter by Severity",
        ["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"]
    )
    filtered_df = display_df[display_df["Severity"].isin(severity_filter)]
    
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )

    # Download
    csv = display_df.to_csv(index=False)
    st.download_button(
        "Download Validation Report (CSV)",
        csv,
        file_name=f"{selected_dataset['filename'].split('.')[0]}_validation_summary.csv",
        mime="text/csv"
    )