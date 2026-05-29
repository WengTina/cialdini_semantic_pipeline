import re


def clean_email_text(text):
    text = str(text).lower()

    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+|www\S+", " URL ", text)
    text = re.sub(r"\S+@\S+", " EMAIL ", text)
    text = re.sub(r"[^a-zA-Z0-9\s!?]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_emails(sample_df, text_col):
    print("Preprocessing email text...")

    sample_df["clean_text"] = sample_df[text_col].apply(clean_email_text)

    sample_df["is_empty_after_cleaning"] = sample_df["clean_text"].apply(
        lambda x: str(x).strip() == ""
    )

    empty_count = sample_df["is_empty_after_cleaning"].sum()

    print(f"Preprocessing completed. Empty cleaned emails: {empty_count}")

    return sample_df