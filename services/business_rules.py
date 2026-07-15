import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join("data", "enterprise_data.db")

class BusinessRules:
    @staticmethod
    def run(df: pd.DataFrame):
        """Run all enabled business rules from SQLite against the provided DataFrame.
        Returns a list of dictionaries, where each dict represents a rule violation:
        {
            "row_number": int,
            "column_name": str,
            "issue_type": str,
            "severity": str,
            "description": str
        }
        """
        violations = []
        
        if not os.path.exists(DB_PATH):
            return violations

        # Connect to DB and fetch active rules
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM business_rules WHERE enabled = 1")
        rules = cursor.fetchall()
        conn.close()
        
        for rule in rules:
            rule_name = rule["rule_name"]
            column_name = rule["column_name"]
            operator = rule["operator"]
            expected_value = rule["expected_value"]
            severity = rule["severity"]
            
            if column_name not in df.columns:
                continue
                
            # Run row by row evaluation
            for idx, value in enumerate(df[column_name]):
                row_num = idx + 1
                is_violation = False
                desc = ""
                
                # Check for nulls first
                is_null = pd.isna(value) or str(value).lower() in ["nan", "none", "null", ""]
                
                if operator == "NOT NULL":
                    if is_null:
                        is_violation = True
                        desc = f"Value is missing in column '{column_name}'."
                elif is_null:
                    # Non-null operators violate rule if value is null
                    is_violation = True
                    desc = f"Value is missing; cannot evaluate rule '{rule_name}'."
                else:
                    try:
                        if operator == ">":
                            if not (float(value) > float(expected_value)):
                                is_violation = True
                                desc = f"Value {value} is not greater than expected threshold {expected_value}."
                        elif operator == "<":
                            if not (float(value) < float(expected_value)):
                                is_violation = True
                                desc = f"Value {value} is not less than expected threshold {expected_value}."
                        elif operator == "=":
                            if not (str(value).strip() == str(expected_value).strip()):
                                is_violation = True
                                desc = f"Value '{value}' does not equal expected value '{expected_value}'."
                        elif operator == "!=":
                            if not (str(value).strip() != str(expected_value).strip()):
                                is_violation = True
                                desc = f"Value '{value}' matches forbidden value '{expected_value}'."
                        elif operator == "IN":
                            allowed_vals = [v.strip() for v in expected_value.split(",")]
                            if str(value).strip() not in allowed_vals:
                                is_violation = True
                                desc = f"Value '{value}' is not in allowed list: {allowed_vals}."
                        elif operator == "<=":
                            if expected_value == "CURRENT_TIME":
                                val_dt = pd.to_datetime(value, errors='coerce')
                                if pd.notna(val_dt) and val_dt > datetime.now():
                                    is_violation = True
                                    desc = f"Timestamp {value} represents a future date/time."
                            else:
                                if not (float(value) <= float(expected_value)):
                                    is_violation = True
                                    desc = f"Value {value} is not less than or equal to {expected_value}."
                        elif operator == ">=":
                            if not (float(value) >= float(expected_value)):
                                is_violation = True
                                desc = f"Value {value} is not greater than or equal to {expected_value}."
                    except ValueError:
                        # Attempt date conversion for comparison operators if numeric fails
                        try:
                            val_dt = pd.to_datetime(value)
                            exp_dt = pd.to_datetime(expected_value)
                            if operator == ">" and not (val_dt > exp_dt):
                                is_violation = True
                                desc = f"Date {value} is not after {expected_value}."
                            elif operator == "<" and not (val_dt < exp_dt):
                                is_violation = True
                                desc = f"Date {value} is not before {expected_value}."
                            elif operator == "<=" and not (val_dt <= exp_dt):
                                is_violation = True
                                desc = f"Date {value} is after {expected_value}."
                            elif operator == ">=" and not (val_dt >= exp_dt):
                                is_violation = True
                                desc = f"Date {value} is before {expected_value}."
                        except Exception:
                            is_violation = True
                            desc = f"Type mismatch: cannot compare '{value}' with expected '{expected_value}' using operator '{operator}'."
                    except Exception as e:
                        is_violation = True
                        desc = f"Evaluation error: {str(e)}."
                        
                if is_violation:
                    violations.append({
                        "row_number": row_num,
                        "column_name": column_name,
                        "issue_type": f"Business Rule: {rule_name}",
                        "severity": severity,
                        "description": desc
                    })
                    
        return violations