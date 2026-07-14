import streamlit as st
import sqlite3
import pandas as pd
from utils.styles import load_css

DB_PATH = "data/enterprise_data.db"

st.set_page_config(
    page_title="Rule Manager",
    layout="wide"
)
# load_css()

st.title("⚙️ Business Rule Manager")

st.markdown("""
Manage enterprise validation rules used during dataset quality checks.
""")

conn = sqlite3.connect(DB_PATH)

rules = pd.read_sql(
    "SELECT * FROM business_rules",
    conn
)

st.subheader("Current Business Rules")

st.dataframe(
    rules,
    use_container_width=True
)

st.divider()

st.subheader("Add New Rule")

with st.form("add_rule"):

    rule_name = st.text_input("Rule Name")

    column_name = st.text_input("Column Name")

    operator = st.selectbox(
        "Operator",
        [
            ">",
            "<",
            "=",
            "!=",
            "IN",
            "NOT NULL"
        ]
    )

    expected_value = st.text_input("Expected Value")

    severity = st.selectbox(
        "Severity",
        [
            "Critical",
            "High",
            "Medium",
            "Low"
        ]
    )

    enabled = st.checkbox(
        "Enable Rule",
        value=True
    )

    submit = st.form_submit_button("Add Rule")

if submit:

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO business_rules(
        rule_name,
        column_name,
        operator,
        expected_value,
        severity,
        enabled
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        rule_name,
        column_name,
        operator,
        expected_value,
        severity,
        int(enabled)
    ))

    conn.commit()

    st.success("Business rule added successfully.")

    st.rerun()

conn.close()