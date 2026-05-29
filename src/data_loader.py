#載入樣本並偵測欄位，抽樣5000筆資料

import os
import random
import numpy as np
import pandas as pd
from datasets import load_dataset

from src.config import (
    DATASET_NAME,
    DATASET_SPLIT,
    RANDOM_STATE,
    SAMPLE_SIZE,
    SAMPLED_EMAILS_PATH,
    OUTPUT_DIR
)


def set_seed():
    random.seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)


def load_email_dataset():
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset(DATASET_NAME)
    df = dataset[DATASET_SPLIT].to_pandas()

    print("Dataset loaded.")
    print("Columns:", df.columns.tolist())
    print("Total rows:", len(df))

    return df


def detect_text_column(df):
    possible_cols = [
        "text", "email", "body", "message", "content",
        "Email Text", "Email", "Email Body", "email_text",
        "email_body", "raw_text"
    ]

    for col in possible_cols:
        if col in df.columns:
            print(f"Detected text column: {col}")
            return col

    raise ValueError(
        "Cannot automatically detect the email text column. "
        f"Available columns are: {df.columns.tolist()}"
    )


def sample_emails(df, text_col):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = df.dropna(subset=[text_col]).reset_index(drop=True)

    if len(df) <= SAMPLE_SIZE:
        sample_df = df.copy()
    else:
        sample_df = df.sample(
            n=SAMPLE_SIZE,
            random_state=RANDOM_STATE
        ).reset_index(drop=True)

    sample_df.insert(0, "email_id", range(1, len(sample_df) + 1))

    sample_df.to_csv(SAMPLED_EMAILS_PATH, index=False, encoding="utf-8-sig")

    print(f"Sampled emails saved to: {SAMPLED_EMAILS_PATH}")
    print("Sample size:", len(sample_df))

    return sample_df