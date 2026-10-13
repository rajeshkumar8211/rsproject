"""Recommendation engine: cosine similarity between a user's skill vector and career profiles.

The CAREER_DATA feature values are the original sample dataset and must not be changed.
Scoring uses sklearn.metrics.pairwise.cosine_similarity only.
CAREER_INFO is display content and does not affect match scores.
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = ["Programming", "Communication", "Creativity", "Mathematics", "Problem Solving"]
SKILL_KEYS = ["programming", "communication", "creativity", "mathematics", "problem_solving"]

# Dataset (unchanged): feature order = SKILLS
CAREER_DATA = {
    "Software Developer": [9, 6, 7, 7, 9],
    "Data Scientist": [8, 6, 6, 10, 10],
    "Data Analyst": [6, 7, 6, 8, 8],
    "UI/UX Designer": [3, 8, 9, 5, 7],
    "Cybersecurity Analyst": [7, 8, 5, 6, 9],
    "Cloud Engineer": [8, 6, 5, 7, 9],
    "Web Developer": [8, 6, 8, 5, 8],
    "Project Manager": [4, 9, 7, 6, 8],
}

CAREER_INFO = {
    "Software Developer": {
        "description": "Designs, builds, and maintains software applications, from mobile apps to backend systems.",
        "key_skills": ["Programming", "Problem Solving", "Creativity"],
        "learn_more": "Explore languages like Python, Java, or JavaScript, build small projects, and learn version control with Git.",
    },
    "Data Scientist": {
        "description": "Uses statistics and machine learning to find patterns in data and predict outcomes.",
        "key_skills": ["Mathematics", "Problem Solving", "Programming"],
        "learn_more": "Study statistics and Python, practise on public datasets (for example on Kaggle), and learn how to evaluate models.",
    },
    "Data Analyst": {
        "description": "Cleans and analyses data, then turns findings into reports and dashboards that guide decisions.",
        "key_skills": ["Mathematics", "Problem Solving", "Communication"],
        "learn_more": "Learn SQL, spreadsheets, and a visualization tool, and practise explaining insights to non-technical people.",
    },
    "UI/UX Designer": {
        "description": "Shapes how products look and feel by researching users and designing clear, usable interfaces.",
        "key_skills": ["Creativity", "Communication", "Problem Solving"],
        "learn_more": "Learn design principles and a tool like Figma, and build a portfolio of redesigned apps with short case studies.",
    },
    "Cybersecurity Analyst": {
        "description": "Protects systems and data by monitoring for threats, finding weaknesses, and responding to incidents.",
        "key_skills": ["Problem Solving", "Communication", "Programming"],
        "learn_more": "Learn networking and Linux basics, try beginner capture-the-flag challenges, and look at entry-level security certifications.",
    },
    "Cloud Engineer": {
        "description": "Builds and runs scalable infrastructure on cloud platforms such as AWS, Azure, or Google Cloud.",
        "key_skills": ["Programming", "Problem Solving", "Mathematics"],
        "learn_more": "Start with a cloud provider's free tier, learn Linux, networking, and infrastructure-as-code, and deploy a small app.",
    },
    "Web Developer": {
        "description": "Creates websites and web apps, combining visual design with front-end and back-end code.",
        "key_skills": ["Programming", "Creativity", "Problem Solving"],
        "learn_more": "Learn HTML, CSS, and JavaScript, then a framework such as React or Flask, and publish a few projects online.",
    },
    "Project Manager": {
        "description": "Plans work, coordinates teams, and keeps projects on schedule and within scope.",
        "key_skills": ["Communication", "Problem Solving", "Creativity"],
        "learn_more": "Practise organising group work, learn agile and planning tools, and consider an entry-level project management certification.",
    },
}

_df = pd.DataFrame.from_dict(CAREER_DATA, orient="index", columns=SKILLS)


def recommend(user_skills, top_n=3):
    """Compare a 5-skill user vector with every career profile using cosine similarity.

    user_skills: list of 5 ints in SKILLS order.
    Returns top_n careers sorted by similarity descending.
    Match percentage = similarity score × 100, formatted to two decimal places.
    """
    if not isinstance(user_skills, (list, tuple)) or len(user_skills) != len(SKILLS):
        raise ValueError("user_skills must contain exactly five values.")

    user_vec = pd.DataFrame([user_skills], columns=SKILLS)
    scores = cosine_similarity(user_vec.values, _df.values)[0]
    result = _df.assign(similarity=scores).sort_values("similarity", ascending=False).head(top_n)

    out = []
    for rank, (career, row) in enumerate(result.iterrows(), start=1):
        info = CAREER_INFO[career]
        sim = float(row["similarity"])
        out.append({
            "rank": rank,
            "career": career,
            "similarity": round(sim, 4),
            "match_percentage": f"{sim * 100:.2f}",
            "description": info["description"],
            "key_skills": info["key_skills"],
            "learn_more": info["learn_more"],
        })
    return out
