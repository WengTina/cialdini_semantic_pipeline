import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

from src.config import (
    TFIDF_MAX_FEATURES,
    TFIDF_NGRAM_RANGE,
    TFIDF_MIN_DF,
    TOP_TFIDF_TERMS_PATH
)

from src.lexicon import CIALDINI_LEXICON, CIALDINI_PRINCIPLES


def compute_tfidf_lexicon_scores(sample_df):
    print("Computing TF-IDF lexicon scores...")

    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        stop_words="english",
        min_df=TFIDF_MIN_DF
    )

    tfidf_matrix = vectorizer.fit_transform(sample_df["clean_text"])
    feature_names = vectorizer.get_feature_names_out()
    feature_index = {term: idx for idx, term in enumerate(feature_names)}

    rows = []

    for i in range(tfidf_matrix.shape[0]):
        row = tfidf_matrix[i]
        scores = {}

        for principle, keywords in CIALDINI_LEXICON.items():
            score = 0.0

            for keyword in keywords:
                keyword = keyword.lower()
                if keyword in feature_index:
                    score += row[0, feature_index[keyword]]

            scores[f"{principle}_tfidf_raw"] = float(score)

        rows.append(scores)

    tfidf_scores = pd.DataFrame(rows)
    sample_df = pd.concat([sample_df, tfidf_scores], axis=1)

    top_terms = pd.DataFrame({
        "term": feature_names,
        "mean_tfidf": np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    }).sort_values("mean_tfidf", ascending=False)

    top_terms.to_csv(TOP_TFIDF_TERMS_PATH, index=False, encoding="utf-8-sig")

    print(f"Top TF-IDF terms saved to: {TOP_TFIDF_TERMS_PATH}")
    print("TF-IDF scoring completed.")

    return sample_df


def normalize_tfidf_scores(sample_df):
    print("Normalizing TF-IDF scores...")

    raw_cols = [f"{p}_tfidf_raw" for p in CIALDINI_PRINCIPLES]
    norm_cols = [f"{p}_tfidf_norm" for p in CIALDINI_PRINCIPLES]

    scaler = MinMaxScaler()
    sample_df[norm_cols] = scaler.fit_transform(sample_df[raw_cols])

    print("TF-IDF normalization completed.")

    return sample_df