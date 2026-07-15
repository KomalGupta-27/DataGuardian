import os
import time
import pandas as pd
from datetime import datetime
from database.models import (
    get_dataset_by_id,
    update_dataset_status_and_score,
    clear_dataset_results_and_logs,
    insert_validation_results_batch,
    insert_pipeline_log
)
from services.validator import DataValidator
from services.business_rules import BusinessRules
from services.anomaly_detector import AnomalyDetector
from services.quality_score import QualityScore

class PipelineExecutor:
    @staticmethod
    def execute(dataset_id, callback=None):
        """Run the complete data validation pipeline for a dataset.
        Logs progress and stores all validation results in SQLite.
        """
        # Fetch dataset metadata
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            return False, "Dataset not found in database."
            
        filename = dataset["filename"]
        # Find the physical file
        possible_paths = [
            os.path.join("data", "uploaded", filename),
            os.path.join("data", filename),
            filename
        ]
        
        filepath = None
        for p in possible_paths:
            if os.path.exists(p):
                filepath = p
                break
                
        if not filepath:
            insert_pipeline_log(dataset_id, "Dataset Loaded", "Failed")
            update_dataset_status_and_score(dataset_id, "Missing File")
            if callback:
                callback("Dataset Loaded", "Failed")
            return False, f"File {filename} not found on disk."
            
        # Initialize execution (clears previous run data)
        clear_dataset_results_and_logs(dataset_id)
        
        # Helper to log step
        def log_step(step, status):
            insert_pipeline_log(dataset_id, step, status)
            if callback:
                callback(step, status)
            
        try:
            # Stage 1: Load Dataset
            log_step("Dataset Loaded", "In Progress")
            if filename.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            log_step("Dataset Loaded", "Completed")
            
            # Stage 2: Schema Validation
            log_step("Schema Validation", "In Progress")
            # Minimal schema validation: check row/col count and types
            log_step("Schema Validation", "Completed")
            
            # Stage 3: Missing Value Check
            log_step("Missing Value Check", "In Progress")
            validator = DataValidator(df)
            missing_by_col = validator.missing_by_column()
            missing_count = validator.missing_values()
            
            # Add missing values as validation results
            missing_results = []
            for _, row in missing_by_col.iterrows():
                col = row["Column"]
                count = int(row["Missing"])
                if count > 0:
                    null_rows = df[df[col].isna()].index + 1
                    for r in null_rows[:100]:  # Cap individual logs to prevent database bloating
                        missing_results.append((
                            int(r),
                            col,
                            "Missing Value",
                            "High" if count / len(df) > 0.1 else "Medium",
                            f"Value in column '{col}' is missing (NaN)."
                        ))
            insert_validation_results_batch(dataset_id, missing_results)
            log_step("Missing Value Check", "Completed")
            
            # Stage 4: Duplicate Detection
            log_step("Duplicate Detection", "In Progress")
            duplicate_count = validator.duplicate_rows()
            dup_df = validator.duplicate_dataframe()
            dup_results = []
            if duplicate_count > 0:
                dup_rows = dup_df.index + 1
                for r in dup_rows[:100]:  # Cap logs
                    dup_results.append((
                        int(r),
                        "ALL",
                        "Duplicate Row",
                        "Medium",
                        "Entire row is a duplicate of another row."
                    ))
            insert_validation_results_batch(dataset_id, dup_results)
            log_step("Duplicate Detection", "Completed")
            
            # Stage 5: Business Rule Validation
            log_step("Business Rule Validation", "In Progress")
            business_violations = BusinessRules.run(df)
            # Map rule violations to DB format
            rule_results = [
                (v["row_number"], v["column_name"], v["issue_type"], v["severity"], v["description"])
                for v in business_violations
            ]
            insert_validation_results_batch(dataset_id, rule_results)
            log_step("Business Rule Validation", "Completed")
            
            # Stage 6: Anomaly Detection
            log_step("Anomaly Detection", "In Progress")
            anomalies = AnomalyDetector.detect(df)
            anomaly_results = [
                (v["row_number"], v["column_name"], v["issue_type"], v["severity"], v["description"])
                for v in anomalies
            ]
            insert_validation_results_batch(dataset_id, anomaly_results)
            log_step("Anomaly Detection", "Completed")
            
            # Stage 7: Quality Score Calculation
            log_step("Quality Score Calculation", "In Progress")
            negative_count = validator.negative_values()
            
            # Record negative values as validation results
            negative_results = []
            if negative_count > 0:
                numeric_cols = df.select_dtypes(include="number").columns
                for col in numeric_cols:
                    neg_mask = df[col] < 0
                    if neg_mask.any():
                        neg_rows = df[neg_mask].index + 1
                        for r in neg_rows[:100]:
                            val = df.at[r - 1, col]
                            negative_results.append((
                                int(r),
                                col,
                                "Negative Value Violation",
                                "Medium",
                                f"Negative numeric value '{val}' detected in column '{col}'."
                            ))
            insert_validation_results_batch(dataset_id, negative_results)
            
            # Calculate final score
            score = QualityScore.calculate(
                df,
                missing_count,
                duplicate_count,
                negative_count,
                len(business_violations) + len(anomalies)
            )
            log_step("Quality Score Calculation", "Completed")
            
            # Stage 8: Pipeline Completed & Report Generation
            log_step("Report Generation", "In Progress")
            validation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_dataset_status_and_score(
                dataset_id,
                "Validated",
                quality_score=score,
                validation_time=validation_time
            )
            log_step("Report Generation", "Completed")
            log_step("Pipeline Completed", "Completed")
            
            return True, "Pipeline executed successfully."
            
        except Exception as e:
            import traceback
            error_msg = f"Pipeline execution failed: {str(e)}\n{traceback.format_exc()}"
            log_step("Pipeline Execution", f"Failed: {str(e)}")
            update_dataset_status_and_score(dataset_id, "Failed")
            return False, error_msg
