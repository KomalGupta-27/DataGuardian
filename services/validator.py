import pandas as pd


class DataValidator:
    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def missing_values(self):
        return int(self.df.isna().sum().sum())

    def missing_by_column(self):
        return pd.DataFrame({
            "Column": self.df.columns,
            "Missing": self.df.isna().sum().values
        })

    def duplicate_rows(self):
        return int(self.df.duplicated().sum())

    def duplicate_dataframe(self):
        return self.df[self.df.duplicated()]

    def empty_columns(self):
        return int((self.df.isna().all()).sum())

    def negative_values(self):
        numeric = self.df.select_dtypes(include="number")

        if numeric.empty:
            return 0

        return int((numeric < 0).sum().sum())

    def numeric_summary(self):
        numeric = self.df.select_dtypes(include="number")

        if numeric.empty:
            return pd.DataFrame()

        return numeric.describe().T

    def column_summary(self):
        return pd.DataFrame({
            "Column": self.df.columns,
            "Data Type": self.df.dtypes.astype(str),
            "Missing": self.df.isna().sum().values,
            "Unique Values": self.df.nunique().values
        })

    def issue_summary(self):
        return {
            "missing": self.missing_values(),
            "duplicates": self.duplicate_rows(),
            "empty_columns": self.empty_columns(),
            "negative_values": self.negative_values()
        }

    def quality_score(self):
        issues = self.issue_summary()

        total = (
            issues["missing"]
            + issues["duplicates"]
            + issues["empty_columns"]
            + issues["negative_values"]
        )

        score = max(0, 100 - min(total, 100))

        return round(score, 2)