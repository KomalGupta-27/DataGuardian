import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from database.models import get_all_datasets, get_connection


# Fetch datasets
datasets = get_all_datasets()
datasets_df = pd.DataFrame(datasets)

# Header
st.title("DataGuardian Dashboard")
st.caption("Data Privacy & Quality Risk Intelligence Registry")
st.divider()

if datasets_df.empty:
    st.info("Welcome to DataGuardian. No datasets have been registered yet. Please upload a dataset to begin.")
    if st.button("Upload a Dataset", type="primary"):
        st.switch_page("app_pages/Upload.py")
    st.stop()

# -----------------------------
# Calculations from Real Database
# -----------------------------
total_files = len(datasets_df)
validated_df = datasets_df[datasets_df["status"] == "Validated"]

if not validated_df.empty:
    avg_quality = round(validated_df["quality_score"].mean(), 1)
    high_risk_count = len(validated_df[validated_df["quality_score"] < 80])
    medium_risk_count = len(validated_df[(validated_df["quality_score"] >= 80) & (validated_df["quality_score"] < 95)])
    low_risk_count = len(validated_df[validated_df["quality_score"] >= 95])
else:
    avg_quality = 0.0
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

# Fetch total issues from validation_results table
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM validation_results")
total_issues_count = cursor.fetchone()[0]

# Fetch recent critical alerts
cursor.execute("""
    SELECT r.filename, v.column_name, v.issue_type, v.severity, v.description
    FROM validation_results v
    JOIN datasets r ON v.dataset_id = r.dataset_id
    WHERE v.severity IN ('Critical', 'High')
    ORDER BY v.result_id DESC
    LIMIT 5
""")
alerts = cursor.fetchall()
conn.close()

# -----------------------------
# KPI Cards (Bento Grid)
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Files Registered",
        str(total_files),
        f"{len(datasets_df[datasets_df['status'] == 'Uploaded'])} pending validation"
    )

with c2:
    st.metric(
        "Issues Detected",
        str(total_issues_count),
        "Across all files"
    )

with c3:
    st.metric(
        "Average Quality",
        f"{avg_quality}%" if avg_quality > 0 else "N/A",
        "Standard threshold: 95.0%"
    )

with c4:
    st.metric(
        "Pending Runs",
        str(len(datasets_df[datasets_df["status"] != "Validated"])),
        "Requires action"
    )

st.write("")

c5, c6, c7 = st.columns(3)

with c5:
    st.metric("High Risk Datasets", str(high_risk_count), "Score < 80%")

with c6:
    st.metric("Medium Risk Datasets", str(medium_risk_count), "Score 80% - 95%")

with c7:
    st.metric("Low Risk Datasets", str(low_risk_count), "Score >= 95%")

st.divider()

# -----------------------------
# Main Layout (Bento Grid)
# -----------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Dataset Registry")
    
    registry_display = datasets_df[["dataset_id", "filename", "upload_timestamp", "total_rows", "quality_score", "status"]].copy()
    registry_display.columns = ["ID", "Filename", "Uploaded At", "Total Rows", "Quality Score", "Pipeline Status"]
    
    # Map percentage to quality score
    registry_display["Quality Score"] = registry_display.apply(
        lambda r: f"{r['Quality Score']}%" if r["Pipeline Status"] == "Validated" else "-",
        axis=1
    )
    
    st.dataframe(
        registry_display,
        width="stretch",
        hide_index=True
    )

with right:
    st.subheader("Active Alerts Log")
    if not alerts:
        st.success("No critical or high severity risks found in the active datasets.")
    else:
        for alert in alerts:
            # Custom styled alert box for a cleaner bento look
            st.markdown(f"""
            <div class="bento-card" style="padding: 15px !important; margin-bottom: 10px !important; border-left: 4px solid #b91c1c !important;">
                <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 600; color: rgba(128,128,128,0.85); margin-bottom: 4px;">
                    {alert['filename']} &middot; Column: {alert['column_name']}
                </div>
                <div style="font-size: 0.9rem; font-weight: 600; margin-bottom: 4px;">
                    {alert['issue_type']} ({alert['severity']})
                </div>
                <div style="font-size: 0.85rem; color: rgba(128,128,128,0.95);">
                    {alert['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# -----------------------------
# Charts Section
# -----------------------------
if not validated_df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dataset Risk Classification")
        risk_dist = pd.DataFrame({
            "Classification": ["High Risk (<80%)", "Medium Risk (80-95%)", "Low Risk (>=95%)"],
            "Count": [high_risk_count, medium_risk_count, low_risk_count]
        })
        risk_dist = risk_dist[risk_dist["Count"] > 0]
        
        if not risk_dist.empty:
            fig = px.bar(
                risk_dist,
                x="Classification",
                y="Count",
                color="Classification",
                text="Count",
                color_discrete_map={
                    "High Risk (<80%)": "#b91c1c",    # Crimson red
                    "Medium Risk (80-95%)": "#d97706", # Muted amber
                    "Low Risk (>=95%)": "#0d9488"      # Steel teal
                }
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
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No validated data available for risk breakdown charts.")

    with col2:
        st.subheader("Data Quality Trends")
        timeline_df = validated_df.sort_values(by="validation_time")
        
        # Color line steel blue/grey
        fig2 = px.line(
            timeline_df,
            x="validation_time",
            y="quality_score",
            hover_name="filename",
            markers=True,
            labels={"validation_time": "Validation Run Time", "quality_score": "Quality Score (%)"}
        )
        fig2.update_traces(line_color="#2563eb", marker=dict(size=8, color="#1e40af"))
        fig2.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Geist, Inter, sans-serif"),
            xaxis=dict(gridcolor="rgba(128,128,128,0.1)"),
            yaxis=dict(gridcolor="rgba(128,128,128,0.1)")
        )
        st.plotly_chart(fig2, width="stretch")

st.divider()
st.caption(
    "DataGuardian Dashboard v1.0 • Privacy Risk & Data Quality Validation Engine"
)