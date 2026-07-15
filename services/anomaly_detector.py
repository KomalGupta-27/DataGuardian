import pandas as pd
import numpy as np

class AnomalyDetector:
    @staticmethod
    def detect(df: pd.DataFrame):
        """Analyze dataset to identify statistical anomalies and risk patterns.
        Returns a list of dicts:
        {
            "row_number": int,
            "column_name": str,
            "issue_type": str,
            "severity": str,
            "description": str
        }
        """
        anomalies = []
        
        # 1. Numerical Outlier Detection (using IQR method)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            # Skip ID columns
            if "id" in col.lower() or col.lower() == "row_number":
                continue
                
            series = df[col].dropna()
            if len(series) < 10:  # Not enough data for robust stats
                continue
                
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
                
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            for idx, value in enumerate(df[col]):
                if pd.isna(value):
                    continue
                row_num = idx + 1
                if value < lower_bound or value > upper_bound:
                    severity = "Medium"
                    # If it's a huge transaction amount, make it High
                    if col.lower() == "transaction_amount" and value > q3 + 3.0 * iqr:
                        severity = "High"
                        
                    anomalies.append({
                        "row_number": row_num,
                        "column_name": col,
                        "issue_type": "Statistical Outlier",
                        "severity": severity,
                        "description": f"Value {value} is outside standard distribution limits. Expected range: [{round(lower_bound, 2)}, {round(upper_bound, 2)}]."
                    })
                    
        # 2. Risk Pattern: High-frequency transaction velocity
        # Check if same customer has >= 3 transactions in 10 minutes
        if "Customer_ID" in df.columns and "Transaction_Time" in df.columns:
            try:
                # Create a copy with datetime
                temp_df = df[["Customer_ID", "Transaction_Time"]].copy()
                temp_df["dt"] = pd.to_datetime(temp_df["Transaction_Time"], errors='coerce')
                temp_df["row_num"] = temp_df.index + 1
                temp_df = temp_df.dropna(subset=["dt"])
                
                # Sort by customer and datetime
                temp_df = temp_df.sort_values(by=["Customer_ID", "dt"])
                
                # Window check
                for customer, group in temp_df.groupby("Customer_ID"):
                    if len(group) < 3:
                        continue
                    
                    # Convert to lists for fast lookup
                    dts = group["dt"].tolist()
                    row_nums = group["row_num"].tolist()
                    times = group["Transaction_Time"].tolist()
                    
                    for i in range(len(dts) - 2):
                        # Difference between i and i+2
                        diff = (dts[i+2] - dts[i]).total_seconds()
                        if diff > 0 and diff <= 600:  # 10 minutes (600 seconds)
                            anomalies.append({
                                "row_number": row_nums[i+2],
                                "column_name": "Transaction_Time",
                                "issue_type": "Velocity Check Failure",
                                "severity": "High",
                                "description": f"Customer {customer} generated 3 transactions within 10 minutes (Range: {times[i]} to {times[i+2]}). Potential rapid-fire transaction risk."
                            })
            except Exception:
                pass
                
        return anomalies
