from flask import Flask, jsonify, render_template, request

from recommender import SKILL_KEYS, recommend

app = Flask(__name__)

DISCLAIMER = (
    "Match percentages show how similar your self-assessed skills are to sample career "
    "profiles. They are not a guarantee of career success, admission, or job outcomes."
)


def validate(payload):
    """Return (list_of_ints, errors). Only integers 1–10 are accepted."""
    if not isinstance(payload, dict):
        return None, {"_": "Request body must be a JSON object."}

    errors, values = {}, []
    for key in SKILL_KEYS:
        v = payload.get(key)
        label = key.replace("_", " ")
        if v is None:
            errors[key] = f"{label} is required."
        elif isinstance(v, bool) or not isinstance(v, int):
            errors[key] = f"{label} must be a whole number from 1 to 10."
        elif not 1 <= v <= 10:
            errors[key] = f"{label} must be an integer from 1 to 10."
        else:
            values.append(v)
    return (values, None) if not errors else (None, errors)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assess")
def assess():
    return render_template("assess.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    payload = request.get_json(silent=True)
    values, errors = validate(payload)
    if errors:
        return jsonify({"error": "Invalid input.", "details": errors}), 400
    try:
        recs = recommend(values)
    except Exception:
        app.logger.exception("Recommendation failed")
        return jsonify({"error": "Something went wrong on our side. Please try again."}), 500
    return jsonify({
        "input": dict(zip(SKILL_KEYS, values)),
        "recommendations": recs,
        "disclaimer": DISCLAIMER,
    })


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found."}), 404
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(_):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Method not allowed."}), 405
    return render_template("404.html"), 405


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
