import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.text_processor import clean_text


def calculate_similarity(resume_text, job_descriptions):
    documents = [resume_text] + job_descriptions

    documents = [
        clean_text(document)
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    )[0]

    return similarities


def rank_jobs(resume_text, jobs_df):
    scores = calculate_similarity(
        resume_text,
        jobs_df["description"].tolist()
    )

    result = jobs_df.copy()

    result["match_score"] = (
        scores * 100
    ).round(2)

    result = result.sort_values(
        "match_score",
        ascending=False
    )

    return result