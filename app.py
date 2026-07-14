import streamlit as st
from utils.styles import load_css

st.set_page_config(
    page_title="DataGuardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load_css()

st.title("DataGuardian")
st.caption("Enterprise Data Quality & Validation Platform")

st.divider()

left, right = st.columns([2, 1])

with left:
    st.markdown("""
### Welcome

DataGuardian is an enterprise-inspired data quality platform that helps analyze,
validate and monitor datasets through an interactive workflow.

The application provides:

- Dataset Upload
- Data Validation
- Business Rule Engine
- Quality Score Analysis
- Report Generation
- Pipeline Monitoring

Use the navigation panel on the left to begin.
""")

with right:

    st.metric("Application Version", "v1.0")

    st.metric("Modules", "7")

    st.metric("Status", "Ready")

st.divider()

st.subheader("Workflow")

st.code("""
Upload Dataset
      │
      ▼
Validate Schema
      │
      ▼
Run Business Rules
      │
      ▼
Calculate Quality Score
      │
      ▼
Generate Reports
      │
      ▼
Export Results
""", language="text")

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.info("Dataset Upload")

with c2:
    st.info("Validation Center")

with c3:
    st.info("Reports & Pipeline")

st.divider()

st.caption("Built using Python • Streamlit • Pandas • Plotly • SQLite")