import streamlit as st
import pandas as pd
import os

from services.business_rules import BusinessRules
from utils.styles import load_css

st.set_page_config(
    page_title="Business Rules",
    layout="wide"
)

load_css()

st.title("Business Rules")
st.caption("Run predefined business validation rules on uploaded datasets.")

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

st.divider()

if st.button("Run Business Rules"):

    results = BusinessRules.run(df)

    if not results:
        st.success("No applicable business rules found for this dataset.")

    else:

        summary = pd.DataFrame({
            "Column": results.keys(),
            "Validation Failures": results.values()
        })

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Rules Executed", len(results))

        with c2:
            st.metric("Total Failures", sum(results.values()))

        st.divider()

        st.subheader("Business Rule Summary")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        csv = summary.to_csv(index=False)

        st.download_button(
            "Download Rule Report",
            csv,
            file_name="business_rule_report.csv",
            mime="text/csv"
        )