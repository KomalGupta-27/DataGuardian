import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "data/enterprise_data.db"


st.title("Business Rule Manager")
st.markdown("""
Configure and manage corporate validation rules used during dataset scans. 
Rules can be enabled/disabled, edited directly, or deleted.
""")

# Load rules from DB
conn = sqlite3.connect(DB_PATH)
rules_df = pd.read_sql("SELECT * FROM business_rules", conn)
conn.close()

# -----------------------------
# Editable Rules Grid
# -----------------------------
st.subheader("Current Rules Configuration")
st.caption("Double-click cells to edit parameters directly, check/uncheck 'enabled' column, then click 'Save Grid Changes' below.")

# Use st.data_editor for inline updates
edited_df = st.data_editor(
    rules_df,
    column_config={
        "rule_id": st.column_config.NumberColumn("Rule ID", disabled=True),
        "rule_name": st.column_config.TextColumn("Rule Name", required=True),
        "column_name": st.column_config.TextColumn("Column Name", required=True),
        "operator": st.column_config.SelectboxColumn(
            "Operator", 
            options=[">", "<", "=", "!=", "IN", "NOT NULL", "<=", ">="],
            required=True
        ),
        "expected_value": st.column_config.TextColumn("Expected Value"),
        "severity": st.column_config.SelectboxColumn(
            "Severity", 
            options=["Critical", "High", "Medium", "Low"],
            required=True
        ),
        "enabled": st.column_config.CheckboxColumn("Enabled", default=True)
    },
    width="stretch",
    hide_index=True
)

c_save1, c_save2 = st.columns([1, 4])
with c_save1:
    if st.button("Save Grid Changes", type="primary"):
        # Save edits back to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Overwrite all entries
        cursor.execute("DELETE FROM business_rules")
        for _, r in edited_df.iterrows():
            cursor.execute("""
                INSERT INTO business_rules (rule_name, column_name, operator, expected_value, severity, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                r["rule_name"],
                r["column_name"],
                r["operator"],
                str(r["expected_value"]),
                r["severity"],
                int(r["enabled"])
            ))
        conn.commit()
        conn.close()
        st.success("Changes saved successfully.")
        st.rerun()

st.divider()

# -----------------------------
# Add New Rule / Delete Actions
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("Create New Business Rule")
    with st.form("add_rule_form", clear_on_submit=True):
        rule_name = st.text_input("Rule Name (e.g. Transaction Limit)")
        column_name = st.text_input("Target Column Name (e.g. Transaction_Amount)")
        operator = st.selectbox(
            "Operator",
            [">", "<", "=", "!=", "IN", "NOT NULL", "<=", ">="]
        )
        expected_value = st.text_input("Expected Value (e.g. 50000 or Approved,Declined)")
        severity = st.selectbox(
            "Violation Severity",
            ["Critical", "High", "Medium", "Low"]
        )
        enabled = st.checkbox("Enable Rule Immediately", value=True)
        
        submit = st.form_submit_button("Add Rule")
        
    if submit:
        if not rule_name or not column_name:
            st.error("Rule Name and Target Column Name are required fields.")
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO business_rules (rule_name, column_name, operator, expected_value, severity, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (rule_name, column_name, operator, expected_value, severity, int(enabled)))
            conn.commit()
            conn.close()
            st.success("Business rule added successfully.")
            st.rerun()

with right:
    st.subheader("Delete Business Rule")
    
    if rules_df.empty:
        st.info("No rules available to delete.")
    else:
        rule_delete_options = {
            f"{r['rule_name']} (Column: {r['column_name']})": r["rule_id"]
            for _, r in rules_df.iterrows()
        }
        
        selected_to_delete = st.selectbox(
            "Select Rule to Remove",
            options=list(rule_delete_options.keys())
        )
        
        delete_btn = st.button("Permanent Delete Rule", type="secondary")
        
        if delete_btn:
            rule_id = rule_delete_options[selected_to_delete]
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM business_rules WHERE rule_id = ?", (rule_id,))
            conn.commit()
            conn.close()
            st.success("Rule successfully deleted.")
            st.rerun()