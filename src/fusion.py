from src.config import ALPHA
from src.lexicon import CIALDINI_PRINCIPLES


def compute_final_scores(sample_df):
    print("Computing final fused scores...")

    for principle in CIALDINI_PRINCIPLES:
        tfidf_col = f"{principle}_tfidf_norm"
        semantic_col = f"{principle}_semantic"
        final_col = f"{principle}_score"

        sample_df[final_col] = (
            ALPHA * sample_df[tfidf_col]
            + (1 - ALPHA) * sample_df[semantic_col]
        )

    print("Final fused scores completed.")
    return sample_df


def build_feature_vector(sample_df):
    print("Building six-dimensional Cialdini vectors...")

    final_cols = [f"{p}_score" for p in CIALDINI_PRINCIPLES]

    sample_df["cialdini_vector"] = sample_df[final_cols].apply(
        lambda row: [round(float(x), 4) for x in row.values],
        axis=1
    )

    def dominant_principles(row, threshold=0.5):
        selected = [
            col.replace("_score", "")
            for col in final_cols
            if row[col] >= threshold
        ]

        if len(selected) == 0:
            top_col = row[final_cols].idxmax()
            selected = [top_col.replace("_score", "")]

        return ";".join(selected)

    sample_df["dominant_principles"] = sample_df.apply(
        dominant_principles,
        axis=1
    )

    print("Feature vector construction completed.")
    return sample_df