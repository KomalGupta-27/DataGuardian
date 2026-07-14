import sqlite3
import os

# Database location
DB_PATH = os.path.join("data", "enterprise_data.db")


def get_connection():
    """Create and return SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Create all required tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # DATASETS TABLE
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_timestamp TEXT,
        uploaded_by TEXT,
        total_rows INTEGER,
        quality_score REAL DEFAULT 0,
        status TEXT,
        validation_time TEXT
    )
    """)

    # -----------------------------
    # VALIDATION RESULTS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS validation_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        row_number INTEGER,
        column_name TEXT,
        issue_type TEXT,
        severity TEXT,
        description TEXT,
        FOREIGN KEY(dataset_id)
        REFERENCES datasets(dataset_id)
    )
    """)

    # -----------------------------
    # BUSINESS RULES
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_rules (
        rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT,
        column_name TEXT,
        operator TEXT,
        expected_value TEXT,
        severity TEXT,
        enabled INTEGER DEFAULT 1
    )
    """)

    # -----------------------------
    # PIPELINE LOGS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        step TEXT,
        status TEXT,
        timestamp TEXT,
        FOREIGN KEY(dataset_id)
        REFERENCES datasets(dataset_id)
    )
    """)

    conn.commit()
    conn.close()


def seed_business_rules():
    """Insert default business rules if table is empty."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM business_rules")
    count = cursor.fetchone()[0]

    if count == 0:

        rules = [

            ("Transaction Amount Positive",
             "Transaction_Amount",
             ">",
             "0",
             "Critical",
             1),

            ("Currency Present",
             "Currency",
             "NOT NULL",
             "",
             "High",
             1),

            ("Country Present",
             "Merchant_Country",
             "NOT NULL",
             "",
             "Medium",
             1),

            ("Future Timestamp Check",
             "Transaction_Time",
             "<=",
             "CURRENT_TIME",
             "Critical",
             1),

            ("Transaction Status Valid",
             "Transaction_Status",
             "IN",
             "Approved,Declined,Pending",
             "High",
             1),

            ("Risk Level Valid",
             "Risk_Level",
             "IN",
             "Low,Medium,High",
             "Medium",
             1),

            ("Card Type Valid",
             "Card_Type",
             "IN",
             "Silver,Gold,Platinum",
             "Medium",
             1)

        ]

        cursor.executemany("""
        INSERT INTO business_rules(
            rule_name,
            column_name,
            operator,
            expected_value,
            severity,
            enabled
        )
        VALUES(?,?,?,?,?,?)
        """, rules)

        conn.commit()

    conn.close()


def initialize_database():
    """Initialize database with tables and rules."""
    create_tables()
    seed_business_rules()


if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    initialize_database()

    print("Database initialized successfully.")