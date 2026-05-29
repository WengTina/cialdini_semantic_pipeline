import pandas as pd

from src.config import QUALITY_REPORT_PATH
from src.lexicon import CIALDINI_PRINCIPLES


def run_quality_check(sample_df):
    print("Running quality check...")

    final_cols = [f"{p}_score" for p in CIALDINI_PRINCIPLES]

    print("\nScore summary:")
    print(sample_df[final_cols].describe())

    print("\nDominant principle counts:")
    print(sample_df["dominant_principles"].value_counts().head(20))

    report = sample_df[final_cols].describe().T
    report.to_csv(QUALITY_REPORT_PATH, encoding="utf-8-sig")

    print(f"Quality report saved to: {QUALITY_REPORT_PATH}")

    return report