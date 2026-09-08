import streamlit as st
import pandas as pd
import plotly.express as px

from pypdf import PdfReader

from src.matcher import rank_jobs
from src.text_processor import extract_skills


st.set_page_config(
    page_title="Resume Job Matcher",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Resume Job Matcher")

st.caption(
    "NLP-powered resume and job description matching system"
)


# --------------------------------------------------
# Load jobs
# --------------------------------------------------

jobs = pd.read_csv("data/jobs.csv")


# --------------------------------------------------
# Skills
# --------------------------------------------------

SKILLS = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "pandas",
    "NumPy",
    "statistics",
    "machine learning",
    "scikit-learn",
    "TensorFlow",
    "PyTorch",
    "deep learning",
    "NLP",
    "NLTK",
    "spaCy",
    "transformers",
    "Docker",
    "Git",
    "AWS",
    "Spark",
    "ETL",
    "DAX",
    "APIs",
    "automation"
]


# --------------------------------------------------
# Resume upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your resume",
    type=["pdf"]
)


resume_text = ""


if uploaded_file:

    try:

        reader = PdfReader(uploaded_file)

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        resume_text = "\n".join(pages)

        st.success(
            "Resume uploaded successfully!"
        )

    except Exception as e:

        st.error(
            f"Could not read the resume: {e}"
        )


# --------------------------------------------------
# Manual resume input
# --------------------------------------------------

st.subheader("📝 Resume Text")

manual_text = st.text_area(
    "You can also paste your resume text here",
    height=200
)


if manual_text.strip():

    resume_text = manual_text


# --------------------------------------------------
# Match jobs
# --------------------------------------------------

if resume_text.strip():

    if st.button(
        "🔍 Find Best Job Matches",
        type="primary"
    ):

        results = rank_jobs(
            resume_text,
            jobs
        )

        st.session_state["results"] = results
        st.session_state["resume_text"] = resume_text


# --------------------------------------------------
# Display results
# --------------------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()

    st.header("🏆 Job Match Results")


    # Top match
    best_job = results.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Best Match",
        best_job["title"]
    )

    c2.metric(
        "Company",
        best_job["company"]
    )

    c3.metric(
        "Match Score",
        f"{best_job['match_score']:.1f}%"
    )


    # --------------------------------------------------
    # Ranking chart
    # --------------------------------------------------

    st.subheader("📊 Job Match Ranking")

    chart = px.bar(
        results,
        x="match_score",
        y="title",
        orientation="h",
        text="match_score",
        labels={
            "match_score": "Match Score (%)",
            "title": "Job Role"
        },
        title="Resume Compatibility by Job"
    )

    chart.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    chart.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )


    # --------------------------------------------------
    # Skills analysis
    # --------------------------------------------------

    st.subheader("🧠 Resume Skill Analysis")

    resume_skills = extract_skills(
        st.session_state["resume_text"],
        SKILLS
    )

    st.write(
        f"Detected **{len(resume_skills)} skills** in your resume."
    )

    if resume_skills:

        st.write(
            "### ✅ Detected Skills"
        )

        st.write(
            ", ".join(resume_skills)
        )


    # --------------------------------------------------
    # Top job details
    # --------------------------------------------------

    st.subheader("💼 Best Matching Job")

    st.write(
        f"**Role:** {best_job['title']}"
    )

    st.write(
        f"**Company:** {best_job['company']}"
    )

    st.write(
        f"**Match Score:** {best_job['match_score']:.1f}%"
    )

    st.write(
        f"**Required Skills:** {best_job['description']}"
    )


    # --------------------------------------------------
    # Complete results
    # --------------------------------------------------

    st.subheader("📋 Complete Ranking")

    display = results[
        [
            "title",
            "company",
            "match_score"
        ]
    ].copy()

    display["match_score"] = display[
        "match_score"
    ].map(
        lambda x: f"{x:.1f}%"
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Upload a PDF resume or paste resume text "
        "to start matching jobs."
    )