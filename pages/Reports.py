import streamlit as st
import pandas as pd
import os
from datetime import datetime

from services.validator import DataValidator
from services.business_rules import BusinessRules
from services.quality_score import QualityScore
from utils.styles import load_css

st.set_page_config(
    page_title="Reports",
    layout="wide"
)

# load_css()

st.title("Reports")
st.caption("Generate and export data quality reports.")

UPLOAD_FOLDER = "data/uploaded"

files = [
    f for f in os.listdir(UPLOAD_FOLDER)
    if f.endswith(".csv") or f.endswith(".xlsx")
] if os.path.exists(UPLOAD_FOLDER) else []

if not files:
    st.warning("No uploaded datasets found.")
    st.stop()

selected = st.selectbox(
    "Select Dataset",
    files
)

path = os.path.join(UPLOAD_FOLDER, selected)

if selected.endswith(".csv"):
    df = pd.read_csv(path)
else:
    df = pd.read_excel(path)

validator = DataValidator(df)

issues = validator.issue_summary()

business = BusinessRules.run(df)
business_failures = sum(business.values())

quality = QualityScore.calculate(
    df,
    issues["missing"],
    issues["duplicates"],
    issues["negative_values"],
    business_failures
)

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("Quality Score", f"{quality}%")
c2.metric("Business Rule Failures", business_failures)
c3.metric("Report Date", datetime.now().strftime("%d %b %Y"))

st.divider()

summary = pd.DataFrame({
    "Metric": [
        "Rows",
        "Columns",
        "Missing Values",
        "Duplicate Rows",
        "Negative Values",
        "Empty Columns",
        "Business Rule Failures",
        "Quality Score"
    ],
    "Value": [
        df.shape[0],
        df.shape[1],
        issues["missing"],
        issues["duplicates"],
        issues["negative_values"],
        issues["empty_columns"],
        business_failures,
        f"{quality}%"
    ]
})

st.subheader("Executive Summary")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

csv = summary.to_csv(index=False)

st.download_button(
    "Export Report (CSV)",
    csv,
    file_name="DataGuardian_Report.csv",
    mime="text/csv"
)

st.success("Report generated successfully.")