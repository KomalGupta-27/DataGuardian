import pandas as pd


class QualityScore:

    WEIGHTS = {
        "missing": 0.35,
        "duplicates": 0.25,
        "negative": 0.20,
        "business": 0.20
    }

    @staticmethod
    def calculate(
        df: pd.DataFrame,
        missing: int,
        duplicates: int,
        negative: int,
        business_failures: int
    ):

        total_cells = max(df.shape[0] * df.shape[1], 1)

        missing_rate = missing / total_cells
        duplicate_rate = duplicates / max(df.shape[0], 1)
        negative_rate = negative / total_cells
        business_rate = business_failures / total_cells

        penalty = (
            missing_rate * QualityScore.WEIGHTS["missing"] +
            duplicate_rate * QualityScore.WEIGHTS["duplicates"] +
            negative_rate * QualityScore.WEIGHTS["negative"] +
            business_rate * QualityScore.WEIGHTS["business"]
        )

        score = round(max(0, (1 - penalty) * 100), 2)

        return score