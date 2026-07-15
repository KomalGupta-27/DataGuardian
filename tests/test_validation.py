import unittest
import pandas as pd
import sqlite3
import os
from services.validator import DataValidator
from services.quality_score import QualityScore
from services.anomaly_detector import AnomalyDetector
from services.business_rules import BusinessRules
import services.business_rules

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        # Create a sample dataframe
        self.df = pd.DataFrame({
            "Transaction_ID": ["TXN001", "TXN002", "TXN003", "TXN001"], # TXN001 is duplicate
            "Customer_ID": ["CUST01", "CUST02", "CUST03", "CUST01"],
            "Transaction_Amount": [100.0, -50.0, 300.0, 100.0], # -50.0 is negative
            "Currency": ["USD", "EUR", None, "USD"], # Row 3 is null
            "Merchant_Country": ["USA", "India", "UK", "USA"],
            "Transaction_Time": ["2026-07-14 10:00:00", "2026-07-14 10:05:00", "2026-07-14 10:10:00", "2026-07-14 10:00:00"]
        })
        
    def test_validator(self):
        validator = DataValidator(self.df)
        self.assertEqual(validator.missing_values(), 1)
        self.assertEqual(validator.duplicate_rows(), 1)
        self.assertEqual(validator.negative_values(), 1)
        
    def test_quality_score(self):
        score = QualityScore.calculate(self.df, 1, 1, 1, 0)
        # Verify score is calculated correctly and is between 0 and 100
        self.assertTrue(0 <= score <= 100)
        
    def test_anomaly_detector(self):
        # Create a df with an obvious outlier for IQR
        df_outlier = pd.DataFrame({
            "Transaction_Amount": [10, 12, 11, 13, 10, 12, 11, 13, 10, 1000] # 1000 is an outlier
        })
        anomalies = AnomalyDetector.detect(df_outlier)
        self.assertTrue(len(anomalies) > 0)
        self.assertEqual(anomalies[0]["column_name"], "Transaction_Amount")
        
    def test_business_rules(self):
        # Use a temporary database for testing rules
        test_db = "data/test_enterprise_data.db"
        original_db = services.business_rules.DB_PATH
        services.business_rules.DB_PATH = test_db
        
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS business_rules")
        cursor.execute("""
            CREATE TABLE business_rules (
                rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT,
                column_name TEXT,
                operator TEXT,
                expected_value TEXT,
                severity TEXT,
                enabled INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            INSERT INTO business_rules (rule_name, column_name, operator, expected_value, severity, enabled)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("Amount Positive", "Transaction_Amount", ">", "0", "Critical", 1))
        conn.commit()
        conn.close()
        
        try:
            violations = BusinessRules.run(self.df)
            self.assertEqual(len(violations), 1)
            self.assertEqual(violations[0]["column_name"], "Transaction_Amount")
            self.assertEqual(violations[0]["row_number"], 2) # Row 2 is -50.0
        finally:
            services.business_rules.DB_PATH = original_db
            if os.path.exists(test_db):
                os.remove(test_db)

if __name__ == "__main__":
    unittest.main()
