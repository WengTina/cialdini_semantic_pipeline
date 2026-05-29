import os

from src.config import OUTPUT_DIR, FINAL_OUTPUT_PATH
from src.data_loader import (
    set_seed,
    load_email_dataset,
    detect_text_column,
    sample_emails
)
from src.preprocess import preprocess_emails
from src.tfidf_scoring import (
    compute_tfidf_lexicon_scores,
    normalize_tfidf_scores
)
from src.semantic_scoring import (
    build_zero_shot_classifier,
    compute_semantic_scores
)
from src.fusion import (
    compute_final_scores,
    build_feature_vector
)
from src.quality_check import run_quality_check
from src.lexicon import CIALDINI_PRINCIPLES


def export_results(sample_df, text_col):
    """
    Export a clean final CSV for Member C.

    The output keeps:
    1. Original Hugging Face dataset columns
    2. Final six Cialdini scores
    3. Six-dimensional Cialdini vector
    4. Dominant principles
    """

    final_score_cols = [
        "reciprocity_score",
        "liking_score",
        "social_proof_score",
        "authority_score",
        "scarcity_score",
        "commitment_consistency_score"
    ]

    final_extra_cols = [
        *final_score_cols,
        "cialdini_vector",
        "dominant_principles"
    ]

    # 保留 Hugging Face 原始欄位，但排除中間計算欄位與本模組新增欄位
    original_cols = [
        col for col in sample_df.columns
        if not (
            col.endswith("_tfidf_raw")
            or col.endswith("_tfidf_norm")
            or col.endswith("_semantic")
            or col.endswith("_score")
            or col in [
                "email_id",
                "clean_text",
                "is_empty_after_cleaning",
                "cialdini_vector",
                "dominant_principles"
            ]
        )
    ]

    output_cols = ["email_id"] + original_cols + final_extra_cols

    # 避免欄位重複，並確保欄位存在於 sample_df
    output_cols = [
        col for i, col in enumerate(output_cols)
        if col in sample_df.columns and col not in output_cols[:i]
    ]

    sample_df[output_cols].to_csv(
        FINAL_OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Clean final output for Member C saved to: {FINAL_OUTPUT_PATH}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    set_seed()

    df = load_email_dataset()
    text_col = detect_text_column(df)

    sample_df = sample_emails(df, text_col)
    sample_df = preprocess_emails(sample_df, text_col)

    sample_df = compute_tfidf_lexicon_scores(sample_df)
    sample_df = normalize_tfidf_scores(sample_df)

    classifier = build_zero_shot_classifier()
    sample_df = compute_semantic_scores(sample_df, classifier)

    sample_df = compute_final_scores(sample_df)
    sample_df = build_feature_vector(sample_df)

    run_quality_check(sample_df)
    export_results(sample_df, text_col)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()