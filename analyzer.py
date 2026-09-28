import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "sql",
    "excel",
    "power bi",
    "data visualization",
    "statistics",
    "nlp",
    "computer vision",
    "django",
    "flask",
    "rest api",
    "git",
    "oops"
]


def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(resume_text):

    resume_text = clean_text(resume_text)

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills


def calculate_similarity(resume_text, job_description):

    documents = [
        clean_text(resume_text),
        clean_text(job_description)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity * 100


def analyze_jobs(resume_text, jobs):

    results = []

    resume_skills = extract_skills(resume_text)

    for job in jobs:

        similarity_score = calculate_similarity(
            resume_text,
            job["description"]
        )

        job_skills = job["skills"]

        matched_skills = []

        missing_skills = []

        for skill in job_skills:

            if skill.lower() in [
                x.lower() for x in resume_skills
            ]:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

        # Skill matching score
        if len(job_skills) > 0:

            skill_score = (
                len(matched_skills) /
                len(job_skills)
            ) * 100

        else:

            skill_score = 0

        # Final score
        final_score = (
            similarity_score * 0.6
            +
            skill_score * 0.4
        )

        results.append({

            "title": job["title"],

            "company": job["company"],

            "location": job["location"],

            "similarity": round(
                similarity_score,
                2
            ),

            "skill_score": round(
                skill_score,
                2
            ),

            "final_score": round(
                final_score,
                2
            ),

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return resume_skills, results