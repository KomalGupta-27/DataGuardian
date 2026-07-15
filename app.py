import streamlit as st
from utils.styles import load_css

st.set_page_config(
    page_title="DataGuardian",
    page_icon=None,
    layout="wide"
)

# Load CSS globally — runs once per session on every page load
load_css()

# Define pages with Material Symbols icons for clean, modern sidebar navigation
welcome_page    = st.Page("app_pages/Welcome.py",         title="Platform Overview",  icon=":material/explore:", default=True)
dashboard_page  = st.Page("app_pages/Dashboard.py",       title="Risk Dashboard",     icon=":material/analytics:")
upload_page     = st.Page("app_pages/Upload.py",          title="Dataset Ingestion",  icon=":material/publish:")
pipeline_page   = st.Page("app_pages/Pipeline_Monitor.py",title="Pipeline Execution", icon=":material/bolt:")
validation_page = st.Page("app_pages/Validation.py",      title="Validation Center",  icon=":material/verified_user:")
rules_page      = st.Page("app_pages/Business_Rules.py",  title="Business Rules Run", icon=":material/fact_check:")
rule_manager    = st.Page("app_pages/Rule_Manager.py",    title="Rule Manager",       icon=":material/rule_folder:")
reports_page    = st.Page("app_pages/Reports.py",         title="Executive Reports",  icon=":material/description:")
settings_page   = st.Page("app_pages/Settings.py",        title="System Settings",    icon=":material/settings:")

# Grouped sidebar navigation
pg = st.navigation(
    {
        "Information":        [welcome_page, dashboard_page],
        "Operations":         [upload_page, pipeline_page],
        "Quality Assurance":  [validation_page, rules_page, rule_manager],
        "Reporting & Config": [reports_page, settings_page],
    },
    position="sidebar",
)

pg.run()