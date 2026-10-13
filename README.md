# Career Path Recommendation System

A student-facing web app that recommends the top 3 career paths based on five self-assessed skills. Matching uses **scikit-learn cosine similarity** against a fixed sample career dataset (Pandas). The UI is Flask templates with Bootstrap 5.

Match percentages are **similarity to sample profiles × 100**, not a prediction of success.

## What was reused from the original Python code

The recommendation engine in `recommender.py` keeps:

- The original eight careers and their five feature values (unchanged).
- `pandas.DataFrame` for the career matrix.
- `sklearn.metrics.pairwise.cosine_similarity` to score the user vector against every career.

Small adaptations for the web app:

- Career descriptions, key skills, and “learn more” text live in `CAREER_INFO` so the API can return them. They do **not** affect scores.
- `recommend()` returns JSON-ready dicts with `match_percentage` formatted to two decimal places (`similarity × 100`).
- Flask (`app.py`) validates that each skill is an **integer from 1 to 10** before calling `recommend()`.

## Project structure

```
app.py                 Flask routes, validation, /api/recommend
recommender.py         Dataset + cosine-similarity engine
requirements.txt
templates/             base, home, assessment, results, 404
static/css/style.css
static/js/assess.js    Slider form + client validation + API call
static/js/results.js   Result cards and progress bars
```

## Run locally

Python 3.10+ recommended.

```bash
cd career-path-recommendation-system
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

- Home: `/`
- Skill assessment: `/assess`
- Results: `/results` (after submitting the form)
- API: `POST /api/recommend`

## Example API request

`POST http://127.0.0.1:5000/api/recommend`  
`Content-Type: application/json`

```json
{
  "programming": 8,
  "communication": 5,
  "creativity": 6,
  "mathematics": 9,
  "problem_solving": 9
}
```

## Example API response

```json
{
  "input": {
    "programming": 8,
    "communication": 5,
    "creativity": 6,
    "mathematics": 9,
    "problem_solving": 9
  },
  "recommendations": [
    {
      "rank": 1,
      "career": "Data Scientist",
      "similarity": 0.9945,
      "match_percentage": "99.45",
      "description": "Uses statistics and machine learning to find patterns in data and predict outcomes.",
      "key_skills": ["Mathematics", "Problem Solving", "Programming"],
      "learn_more": "Study statistics and Python, practise on public datasets (for example on Kaggle), and learn how to evaluate models."
    }
  ],
  "disclaimer": "Match percentages show how similar your self-assessed skills are to sample career profiles. They are not a guarantee of career success, admission, or job outcomes."
}
```

(The response includes three careers, sorted by similarity descending.)

Invalid input returns **HTTP 400**:

```json
{
  "error": "Invalid input.",
  "details": {
    "mathematics": "mathematics must be an integer from 1 to 10."
  }
}
```

Keys must be integers 1–10: `programming`, `communication`, `creativity`, `mathematics`, `problem_solving`. Floats, strings, and missing fields are rejected.

## Skill and career dataset

| Career | Programming | Communication | Creativity | Mathematics | Problem Solving |
| --- | --- | --- | --- | --- | --- |
| Software Developer | 9 | 6 | 7 | 7 | 9 |
| Data Scientist | 8 | 6 | 6 | 10 | 10 |
| Data Analyst | 6 | 7 | 6 | 8 | 8 |
| UI/UX Designer | 3 | 8 | 9 | 5 | 7 |
| Cybersecurity Analyst | 7 | 8 | 5 | 6 | 9 |
| Cloud Engineer | 8 | 6 | 5 | 7 | 9 |
| Web Developer | 8 | 6 | 8 | 5 | 8 |
| Project Manager | 4 | 9 | 7 | 6 | 8 |
