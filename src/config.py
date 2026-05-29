#統一管理模型

import os

# Reproducibility
RANDOM_STATE = 42

# Dataset
DATASET_NAME = "lleratodev/ai-powered-phishing-email-detection-system"
DATASET_SPLIT = "train"

# Sampling
SAMPLE_SIZE = 5000

# 第一次測試建議設成 100；確認成功後改成 None 跑完整 5000 筆
#SEMANTIC_LIMIT = 100
SEMANTIC_LIMIT = None

# TF-IDF settings
TFIDF_MAX_FEATURES = 10000
TFIDF_NGRAM_RANGE = (1, 3)
TFIDF_MIN_DF = 1

# Zero-shot model
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

# Fusion weight
# final_score = ALPHA * tfidf_score + (1 - ALPHA) * semantic_score
ALPHA = 0.4

# Output paths
OUTPUT_DIR = "outputs"
SAMPLED_EMAILS_PATH = os.path.join(OUTPUT_DIR, "sampled_emails.csv")
TOP_TFIDF_TERMS_PATH = os.path.join(OUTPUT_DIR, "top_tfidf_terms.csv")
FINAL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "cialdini_feature_vectors.csv")
QUALITY_REPORT_PATH = os.path.join(OUTPUT_DIR, "quality_report.csv")