import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.styles import load_css

st.set_page_config(page_title="Validation Center", layout="wide")
# load_css()

st.title("Validation Center")
st.caption("Analyze uploaded datasets for data quality issues.")

UPLOAD_FOLDER = "data/uploaded"

files = []

if os.path.exists(UPLOAD_FOLDER):
    files = [
        f for f in os.listdir(UPLOAD_FOLDER)
        if f.endswith(".csv") or f.endswith(".xlsx")
    ]

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

# -----------------------
# Validation Summary
# -----------------------

missing = int(df.isna().sum().sum())
duplicates = int(df.duplicated().sum())

empty_columns = int((df.isna().all()).sum())

numeric = df.select_dtypes(include="number")

negative_values = 0

if not numeric.empty:
    negative_values = int((numeric < 0).sum().sum())

total_issues = (
    missing
    + duplicates
    + empty_columns
    + negative_values
)

quality = max(
    0,
    100 - min(total_issues, 100)
)

# -----------------------
# KPI Cards
# -----------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Quality Score", f"{quality}%")
c2.metric("Missing Values", missing)
c3.metric("Duplicate Rows", duplicates)
c4.metric("Negative Values", negative_values)

st.divider()

# -----------------------
# Charts
# -----------------------

left, right = st.columns(2)

with left:

    chart = pd.DataFrame({
        "Issue": [
            "Missing",
            "Duplicates",
            "Negative Values",
            "Empty Columns"
        ],
        "Count": [
            missing,
            duplicates,
            negative_values,
            empty_columns
        ]
    })

    fig = px.bar(
        chart,
        x="Issue",
        y="Count",
        color="Issue",
        text="Count"
    )

    fig.update_layout(
        height=380,
        showlegend=False
    )

    st.subheader("Validation Issues")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    pie = px.pie(
        chart,
        names="Issue",
        values="Count",
        hole=.55
    )

    pie.update_layout(height=380)

    st.subheader("Issue Distribution")

    st.plotly_chart(
        pie,
        use_container_width=True
    )

st.divider()

# -----------------------
# Missing Values
# -----------------------

st.subheader("Missing Values by Column")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing": df.isna().sum().values
})

st.dataframe(
    missing_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------
# Duplicate Records
# -----------------------

st.subheader("Duplicate Records")

dup = df[df.duplicated()]

if dup.empty:
    st.success("No duplicate records found.")
else:
    st.dataframe(
        dup,
        use_container_width=True
    )

st.divider()

# -----------------------
# Dataset Preview
# -----------------------

st.subheader("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# -----------------------
# Download
# -----------------------

csv = missing_df.to_csv(index=False)

st.download_button(
    "Download Validation Summary",
    csv,
    file_name="validation_summary.csv",
    mime="text/csv"
)