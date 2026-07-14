import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import load_css
st.set_page_config(
    page_title="DataGuardian",
    page_icon="🛡️",
    layout="wide"
)
# load_css()

# -----------------------------
# Sample Data
# -----------------------------
recent_scans = pd.DataFrame({
    "File": [
        "customer_data.csv",
        "sales_report.xlsx",
        "employees.pdf",
        "transactions.csv",
        "backup.zip"
    ],
    "Type": [
        "CSV",
        "Excel",
        "PDF",
        "CSV",
        "ZIP"
    ],
    "Risk": [
        "High",
        "Low",
        "Medium",
        "High",
        "Low"
    ],
    "Status": [
        "Flagged",
        "Safe",
        "Review",
        "Flagged",
        "Safe"
    ],
    "Time": [
        "10 min ago",
        "30 min ago",
        "1 hour ago",
        "Yesterday",
        "Yesterday"
    ]
})

risk_distribution = pd.DataFrame({
    "Risk": ["High", "Medium", "Low"],
    "Count": [4, 7, 18]
})

# -----------------------------
# Header
# -----------------------------
st.title("DataGuardian")
st.caption("Data Privacy & Risk Intelligence Dashboard")

st.divider()

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Files Scanned",
        "248",
        "+18 Today"
    )

with c2:
    st.metric(
        "Risks Detected",
        "17",
        "-2"
    )

with c3:
    st.metric(
        "Safe Files",
        "231",
        "+20"
    )

with c4:
    st.metric(
        "Compliance Score",
        "93%",
        "+1.5%"
    )

st.write("")

c5, c6, c7 = st.columns(3)

with c5:
    st.metric(
        "High Risk",
        "4"
    )

with c6:
    st.metric(
        "Medium Risk",
        "5"
    )

with c7:
    st.metric(
        "Low Risk",
        "8"
    )

st.divider()

# -----------------------------
# Main Layout
# -----------------------------
left, right = st.columns([2, 1])

# -----------------------------
# Recent Activity
# -----------------------------
with left:

    st.subheader("Recent Scan Activity")

    st.dataframe(
        recent_scans,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# Alerts
# -----------------------------
with right:

    st.subheader("Recent Alerts")

    st.warning("Customer names detected")

    st.warning("Email addresses detected")

    st.warning("PAN numbers detected")

    st.info("1 report pending review")

st.divider()

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("Risk Distribution")

    fig = px.bar(
        risk_distribution,
        x="Risk",
        y="Count",
        color="Risk",
        text="Count",
        color_discrete_map={
            "High": "#DC2626",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
    )

    fig.update_layout(
        height=380,
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Overall Risk Share")

    fig2 = px.pie(
        risk_distribution,
        names="Risk",
        values="Count",
        hole=0.55,
        color="Risk",
        color_discrete_map={
            "High": "#DC2626",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
    )

    fig2.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "DataGuardian v1.0 • Privacy Risk Detection • Built with Streamlit"
)