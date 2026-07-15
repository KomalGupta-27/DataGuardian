import streamlit as st
import pandas as pd
import os
import sqlite3

from services.business_rules import BusinessRules



st.title("Business Rule Executions")
st.caption("Run predefined corporate business validation rules on uploaded datasets.")

UPLOAD_FOLDER = "data/uploaded"

files = []
if os.path.exists(UPLOAD_FOLDER):
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".csv") or f.endswith(".xlsx")
    ]

if not files:
    st.warning("No uploaded datasets found. Please upload a dataset first.")
    st.stop()

selected = st.selectbox(
    "Select Dataset to Evaluate",
    files
)

path = os.path.join(UPLOAD_FOLDER, selected)

if selected.endswith(".csv"):
    df = pd.read_csv(path)
else:
    df = pd.read_excel(path)

st.divider()

if st.button("Run Business Rules", type="primary"):
    violations = BusinessRules.run(df)
    
    if not violations:
        st.success("All business rules passed. No issues detected.")
    else:
        violations_df = pd.DataFrame(violations)
        
        col_summary = violations_df.groupby("column_name").size().reset_index(name="Failure Count")
        col_summary.rename(columns={"column_name": "Column"}, inplace=True)
        
        c1, c2 = st.columns(2)
        c1.metric("Rules Violations Detected", len(violations_df))
        c2.metric("Affected Columns", len(col_summary))
        
        st.divider()
        
        st.subheader("Failures Summary by Column")
        st.dataframe(
            col_summary,
            width="stretch",
            hide_index=True
        )
        
        st.subheader("Detailed Violations Log")
        display_df = violations_df[["row_number", "column_name", "severity", "description"]].copy()
        display_df.columns = ["Row", "Column", "Severity", "Description"]
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )
        
        csv = violations_df.to_csv(index=False)
        st.download_button(
            "Download Detailed Rule Report (CSV)",
            csv,
            file_name=f"{selected.split('.')[0]}_business_rule_failures.csv",
            mime="text/csv"
        )
