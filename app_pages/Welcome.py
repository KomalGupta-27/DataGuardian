import streamlit as st


st.title("DataGuardian")
st.caption("Enterprise Data Quality & Risk Decision Pipeline Validation Platform")
st.divider()

# Bento Grid layout for Welcome and Platform Overview
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
    <div class="bento-card" style="height: 100%;">
        <div class="bento-header">System Overview</div>
        <div class="bento-value" style="font-size: 1.8rem !important; margin-bottom: 12px;">Enterprise Data Quality Management</div>
        <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-color); margin-bottom: 12px;">
            DataGuardian is a high-performance data quality platform designed for validation, business logic enforcement, and risk detection. The system runs an automated validation pipeline to produce comprehensive data quality metrics, helping product managers and risk analysts make secure, data-driven decisions.
        </p>
        <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-color);">
            Navigate using the sidebar to ingest datasets, define rule logic, run the execution pipeline, and export audited compliance summaries.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 15px;">
        <div class="bento-header">Application Status</div>
        <div class="bento-value" style="font-size: 1.8rem !important; color: #10B981;">Active</div>
        <div class="bento-desc">All validation engines online</div>
    </div>
    <div class="bento-card">
        <div class="bento-header">System Version</div>
        <div class="bento-value" style="font-size: 1.8rem !important;">1.0.0</div>
        <div class="bento-desc">Enterprise Stable Build</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("Platform Architecture and Modules")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="bento-card" style="height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div class="bento-header">Module 01</div>
            <div class="bento-value" style="font-size: 1.3rem !important; margin-bottom: 8px;">Dataset Upload</div>
            <div class="bento-desc" style="font-size: 0.85rem; line-height: 1.5;">
                Ingest transaction logs or customer lists. Checks schemas and initializes database registration.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Ingestion", key="nav_upload_welcome", width="stretch"):
        st.switch_page("app_pages/Upload.py")

with c2:
    st.markdown("""
    <div class="bento-card" style="height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div class="bento-header">Module 02</div>
            <div class="bento-value" style="font-size: 1.3rem !important; margin-bottom: 8px;">Pipeline Monitor</div>
            <div class="bento-desc" style="font-size: 0.85rem; line-height: 1.5;">
                Execute and monitor validation stages in real-time. Logs validation milestones to SQLite.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Pipeline", key="nav_pipeline_welcome", width="stretch"):
        st.switch_page("app_pages/Pipeline_Monitor.py")

with c3:
    st.markdown("""
    <div class="bento-card" style="height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div class="bento-header">Module 03</div>
            <div class="bento-value" style="font-size: 1.3rem !important; margin-bottom: 8px;">Risk & Reports</div>
            <div class="bento-desc" style="font-size: 0.85rem; line-height: 1.5;">
                Access executive summaries and audit histories. Download detailed CSV failure matrices.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Reporting", key="nav_reports_welcome", width="stretch"):
        st.switch_page("app_pages/Reports.py")

st.divider()

st.subheader("Data Validation Lifecycle")
st.code("""
Upload Dataset  ──>  Validate Schema  ──>  Evaluate Business Rules  ──>  Detect Statistical Outliers  ──>  Calculate Quality Score  ──>  Generate Executive Reports
""", language="text")

st.divider()
st.caption("DataGuardian Enterprise • Built with Python, Streamlit, Pandas, Plotly, and SQLite")
