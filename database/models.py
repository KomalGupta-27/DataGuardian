import sqlite3
import os
from datetime import datetime
from database.database import get_connection

def get_all_datasets():
    """Retrieve all datasets sorted by latest upload."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets ORDER BY upload_timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_dataset_by_id(dataset_id):
    """Retrieve a single dataset by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets WHERE dataset_id = ?", (dataset_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_dataset_by_name(filename):
    """Retrieve a single dataset by filename."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datasets WHERE filename = ? ORDER BY upload_timestamp DESC LIMIT 1", (filename,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def insert_dataset(filename, total_rows, status="Uploaded", quality_score=0.0):
    """Insert a new dataset metadata entry and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    upload_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO datasets (filename, upload_timestamp, uploaded_by, total_rows, quality_score, status, validation_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (filename, upload_timestamp, "System", total_rows, quality_score, status, None))
    dataset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return dataset_id

def update_dataset_status_and_score(dataset_id, status, quality_score=None, validation_time=None):
    """Update dataset status, quality score, and validation time."""
    conn = get_connection()
    cursor = conn.cursor()
    if quality_score is not None and validation_time is not None:
        cursor.execute("""
            UPDATE datasets 
            SET status = ?, quality_score = ?, validation_time = ?
            WHERE dataset_id = ?
        """, (status, quality_score, validation_time, dataset_id))
    elif quality_score is not None:
        cursor.execute("""
            UPDATE datasets 
            SET status = ?, quality_score = ?
            WHERE dataset_id = ?
        """, (status, quality_score, dataset_id))
    else:
        cursor.execute("""
            UPDATE datasets 
            SET status = ?
            WHERE dataset_id = ?
        """, (status, dataset_id))
    conn.commit()
    conn.close()

def clear_dataset_results_and_logs(dataset_id):
    """Delete existing validation results and pipeline logs for a dataset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM validation_results WHERE dataset_id = ?", (dataset_id,))
    cursor.execute("DELETE FROM pipeline_logs WHERE dataset_id = ?", (dataset_id,))
    conn.commit()
    conn.close()

def insert_validation_result(dataset_id, row_number, column_name, issue_type, severity, description):
    """Insert a single data validation or business rule failure result."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO validation_results (dataset_id, row_number, column_name, issue_type, severity, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, row_number, column_name, issue_type, severity, description))
    conn.commit()
    conn.close()

def insert_validation_results_batch(dataset_id, results):
    """Insert multiple validation results in a single transaction.
    results is a list of tuples: (row_number, column_name, issue_type, severity, description)
    """
    if not results:
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO validation_results (dataset_id, row_number, column_name, issue_type, severity, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(dataset_id, r[0], r[1], r[2], r[3], r[4]) for r in results])
    conn.commit()
    conn.close()

def get_validation_results(dataset_id):
    """Retrieve all validation results for a dataset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM validation_results WHERE dataset_id = ?", (dataset_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_business_rules(only_enabled=True):
    """Retrieve business rules from database."""
    conn = get_connection()
    cursor = conn.cursor()
    if only_enabled:
        cursor.execute("SELECT * FROM business_rules WHERE enabled = 1")
    else:
        cursor.execute("SELECT * FROM business_rules")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_pipeline_log(dataset_id, step, status):
    """Log a step in the pipeline execution."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO pipeline_logs (dataset_id, step, status, timestamp)
        VALUES (?, ?, ?, ?)
    """, (dataset_id, step, status, timestamp))
    conn.commit()
    conn.close()

def get_pipeline_logs(dataset_id):
    """Retrieve all pipeline logs for a dataset sorted by execution time."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pipeline_logs WHERE dataset_id = ? ORDER BY log_id ASC", (dataset_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
