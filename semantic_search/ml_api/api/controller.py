import numpy as np
from flask import jsonify, request
from ml_api.api.config import APP_NAME
from prometheus_client import Gauge, Histogram, Info
# sys.path.append("../semantic_search/semsearch_pkg/")
from semsearch.predict import make_predictions

PREDICTION_TRACKER = Histogram(
    name="similarity_prediction",
    documentation="ML Model Prediction on House Price",
    labelnames=["app_name", "model_name", "model_version"],
)

PREDICTION_GAUGE = Gauge(
    name="similarity_gauge",
    documentation="ML Model Prediction on House Price for min max calcs",
    labelnames=["app_name", "model_name", "model_version"],
)

MODEL_VERSIONS = Info(
    "model_version_details",
    "Capture model version information",
)

MODEL_VERSIONS.info(
    {
        "live_model": "Clip",
        "live_version": "0.1.0",
        "shadow_model": "Clip_Shadow",
        "shadow_version": "0.1.1",
    }
)


def health():
    if request.method == "GET":
        return jsonify({"status": "ok"})


def predict():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        print("POST:", json_data)

        # Step 2: Access the model prediction function (also validates data)
        result = make_predictions(input_data=json_data)
        # Step 3: Handle errors
        # errors = result.get("errors")
        # if errors:
        #     return Response(json.dumps(errors), status=400)

        # # Step 4: Split out results
        # predictions = result.get("predictions").tolist()
        # version = result.get("version")

        # Step 4: Monitoring
        # for _prediction in result:
        if result:
            scores = [i["score"] for i in result]
            mean_score = np.mean(scores)
        else:
            mean_score = 0
        PREDICTION_TRACKER.labels(
            app_name=APP_NAME, model_name="Clip", model_version="0.1.0"
        ).observe(mean_score)
        PREDICTION_GAUGE.labels(
            app_name=APP_NAME, model_name="Clip", model_version="0.1.0"
        ).set(mean_score)

        # Step 5: Prepare prediction response
        return jsonify(
            {"predictions": result, "version": "0.1.0", "errors": []})
