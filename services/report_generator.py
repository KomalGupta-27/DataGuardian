import pandas as pd
from database.models import get_dataset_by_id, get_validation_results

class ReportGenerator:
    @staticmethod
    def generate_markdown_summary(dataset_id):
        """Generates a structured markdown report summary for a dataset."""
        dataset = get_dataset_by_id(dataset_id)
        if not dataset:
            return "# Executive Report\nDataset not found."
            
        results = get_validation_results(dataset_id)
        
        # Count issues
        total_issues = len(results)
        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        type_counts = {}
        
        for r in results:
            severity = r.get("severity", "Medium")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            issue_type = r.get("issue_type", "Validation Issue")
            type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
            
        report = []
        report.append(f"# Executive Data Quality & Risk Report")
        report.append(f"**Dataset Name:** `{dataset['filename']}`")
        report.append(f"**Scan Executed:** {dataset['validation_time'] or 'Not Scanned'}")
        report.append(f"**Total Records Analyzed:** {dataset['total_rows']:,}")
        report.append(f"**Overall Quality Score:** {dataset['quality_score']}%")
        report.append("")
        report.append("## Executive Summary")
        if dataset['quality_score'] >= 95:
            report.append("STANDARD PASS: The dataset meets the enterprise data quality standard (>= 95% Quality). It is safe to proceed to downstream decision pipelines.")
        elif dataset['quality_score'] >= 80:
            report.append("CONDITIONAL PASS: Minor validation issues detected. Review is recommended before using this dataset in sensitive production models.")
        else:
            report.append("STANDARD FAIL: Critical risk thresholds breached. This dataset contains significant data quality issues and should NOT be processed.")
            
        report.append("")
        report.append("## Validation Issues by Severity")
        report.append("| Severity | Issue Count |")
        report.append("| --- | --- |")
        for sev, count in severity_counts.items():
            report.append(f"| {sev} | {count} |")
            
        report.append("")
        report.append("## Issues breakdown by Category")
        if type_counts:
            report.append("| Issue Category | Failure Count |")
            report.append("| --- | --- |")
            for itype, count in type_counts.items():
                report.append(f"| {itype} | {count} |")
        else:
            report.append("*No validation failures detected.*")
            
        return "\n".join(report)
        
    @staticmethod
    def generate_csv_report(dataset_id):
        """Generates a CSV string representation of all validation issues for download."""
        results = get_validation_results(dataset_id)
        if not results:
            return "Row Number,Column Name,Issue Type,Severity,Description\nN/A,N/A,No Issues,Low,All validations passed"
            
        df = pd.DataFrame(results)
        cols_to_keep = ["row_number", "column_name", "issue_type", "severity", "description"]
        existing_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[existing_cols]
        df.columns = [c.replace("_", " ").title() for c in existing_cols]
        return df.to_csv(index=False)
