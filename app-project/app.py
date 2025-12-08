from flask import Flask, request, jsonify, abort
from analyzer import analyze

app = Flask(__name__)


@app.route("/analyze", methods=["GET", "POST"])
def analyze_route():
    """
    API Endpoint:
        /analyze
    Methods:
        GET  - /analyze?place=San Francisco&year=2020
        POST - JSON { "place": "...", "year": "..." }
    """
    # ---------------------------
    # Parse GET parameters
    # ---------------------------
    if request.method == "GET":
        place = request.args.get("place")
        year = request.args.get("year")

    # ---------------------------
    # Parse POST JSON body
    # ---------------------------
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        place = data.get("place")
        year = data.get("year")

    # ---------------------------
    # Validate parameters
    # ---------------------------
    if not place or not year:
        return jsonify({
            "error": "Both 'place' and 'year' are required."
        }), 400

    # ---------------------------
    # Analyze data
    # ---------------------------
    result_array = analyze(place, year)

    if result_array.size == 0:
        return jsonify({
            "place": place,
            "year": year,
            "message": "No data found"
        }), 404

    # ---------------------------
    # Return numeric results
    # ---------------------------
    return jsonify({
        "place": place,
        "year": year,
        "positive_counts": result_array.tolist(),
        "total_cases": float(result_array.sum()),
        "average_cases": float(result_array.mean()),
        "max_cases": float(result_array.max()),
        "min_cases": float(result_array.min())
    })


if __name__ == "__main__":
    app.run(debug=True)
