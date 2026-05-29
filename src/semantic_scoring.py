import os
import torch
import pandas as pd
from tqdm import tqdm
from transformers import pipeline

from src.config import ZERO_SHOT_MODEL, SEMANTIC_LIMIT, OUTPUT_DIR
from src.lexicon import CANDIDATE_LABELS, LABEL_TO_PRINCIPLE


CHECKPOINT_PATH = os.path.join(OUTPUT_DIR, "semantic_scores_checkpoint.csv")


def build_zero_shot_classifier():
    device = 0 if torch.cuda.is_available() else -1

    print(f"Loading zero-shot model: {ZERO_SHOT_MODEL}")
    classifier = pipeline(
        "zero-shot-classification",
        model=ZERO_SHOT_MODEL,
        device=device
    )

    print("Using device:", "GPU" if device == 0 else "CPU")
    return classifier


def empty_score_row():
    row = {}
    for principle in LABEL_TO_PRINCIPLE.values():
        row[f"{principle}_semantic"] = 0.0
    return row


def compute_semantic_scores(sample_df, classifier):
    print("Computing zero-shot semantic scores...")

    if SEMANTIC_LIMIT is not None:
        print(f"Pilot mode: only processing first {SEMANTIC_LIMIT} emails.")
        sample_df = sample_df.iloc[:SEMANTIC_LIMIT].reset_index(drop=True)

    # 如果之前有 checkpoint，就從中斷處繼續
    if os.path.exists(CHECKPOINT_PATH):
        checkpoint_df = pd.read_csv(CHECKPOINT_PATH)
        start_idx = len(checkpoint_df)
        rows = checkpoint_df.to_dict("records")
        print(f"Found checkpoint. Resuming from index {start_idx}.")
    else:
        start_idx = 0
        rows = []

    texts = sample_df["clean_text"].tolist()

    for idx in tqdm(range(start_idx, len(texts)), desc="Zero-shot scoring"):
        text = texts[idx]

        # 防止空字串、NaN、None 造成錯誤
        if pd.isna(text) or str(text).strip() == "":
            rows.append(empty_score_row())
            continue

        text = str(text).strip()

        try:
            result = classifier(
                text[:1500],
                candidate_labels=CANDIDATE_LABELS,
                multi_label=True,
                hypothesis_template="This email uses the persuasion principle of {}."
            )

            label_score_map = dict(zip(result["labels"], result["scores"]))

            row = {}
            for label, principle in LABEL_TO_PRINCIPLE.items():
                row[f"{principle}_semantic"] = float(label_score_map.get(label, 0.0))

            rows.append(row)

        except Exception as e:
            print(f"\nError at index {idx}. Email skipped.")
            print(f"Error message: {e}")
            rows.append(empty_score_row())

        # 每 50 筆存一次 checkpoint，避免白跑
        if (idx + 1) % 50 == 0:
            pd.DataFrame(rows).to_csv(
                CHECKPOINT_PATH,
                index=False,
                encoding="utf-8-sig"
            )

    semantic_scores = pd.DataFrame(rows)

    # 最後再存一次完整 checkpoint
    semantic_scores.to_csv(
        CHECKPOINT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    sample_df = sample_df.iloc[:len(semantic_scores)].reset_index(drop=True)
    sample_df = pd.concat([sample_df, semantic_scores], axis=1)

    print("Semantic scoring completed.")
    return sample_df