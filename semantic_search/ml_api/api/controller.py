import sys

from flask import Response, jsonify, request

sys.path.append("../semantic_search/semsearch_pkg/")
import json

from semsearch.predict import make_predictions


def health():
    if request.method == "GET":
        return jsonify({"status": "ok"})


def predict():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_predictions(input_data=json_data)
        # Step 3: Handle errors
        # errors = result.get("errors")
        # if errors:
        #     return Response(json.dumps(errors), status=400)

        # # Step 4: Split out results
        # predictions = result.get("predictions").tolist()
        # version = result.get("version")

        # Step 5: Prepare prediction response
        return jsonify({"predictions": result, "version": "0.1.0", "errors": []})
