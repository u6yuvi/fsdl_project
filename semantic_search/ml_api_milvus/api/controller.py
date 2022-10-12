import base64
import time
from io import BytesIO

import flask
import numpy as np
import requests
from flask import jsonify, request
from ml_api_milvus.api.config import APP_NAME
from PIL import Image
import base64
from io import BytesIO
import requests
from ml_api_milvus.api.persistence.data_access import PredictionPersistence, ModelType

from prometheus_client import Gauge, Histogram, Info

# sys.path.append("../semantic_search/semsearch_pkg/")
# from semsearch.predict import make_predictions

PREDICTION_TRACKER = Histogram(
    name="similarity_prediction",
    documentation="ML Model Prediction on similarity",
    labelnames=["app_name", "model_name", "model_version"],
)

PREDICTION_GAUGE = Gauge(
    name="similarity_gauge",
    documentation="ML Model Prediction on House Price for min max calcs",
    labelnames=["app_name", "model_name", "model_version"],
)

PREDICTION_LATENCY = Histogram(
    name="similarity_search_latency",
    documentation="latency on similarity search",
    labelnames=["app_name", "model_name", "model_version"],
)

LATENCY_GAUGE = Gauge(
    name="similarity_search_latency_gauge",
    documentation="Search latency min/max",
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


def get_text_embeddings(query):
    query_emb = flask.g.model.encode(
        [query], convert_to_tensor=True, show_progress_bar=False
    )
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
    return query_emb.detach().numpy()


def make_predictions(input_data):
    query_text = input_data
    query_embed = get_text_embeddings(query_text)
    vectors_to_search = [query_embed[0]]
    search_params = {
        "metric_type": "IP",
        "params": {"nprobe": 10},
    }

    start_time = time.time()
    result = flask.g.fsdl_ip.search(
        vectors_to_search,
        "embeddings",
        search_params,
        limit=3,
        output_fields=["img_name"],
    )
    end_time = time.time()
    latency = end_time - start_time
    hit_list = []
    redis = flask.g.redis
    for hits in result:
        for h in hits:
            hh = {}
            # Currently this returns the image as uri
            # If the images are available online, this can be changed to url
            name = h.entity.get("img_name")
            img_url = (
                "https://storage.googleapis.com/fsdl_images/semsearch/"
                + name
                + ".jpg"
            )
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            # img = Image.open(img_url)
            data = BytesIO()
            img.save(data, "JPEG")
            data64 = base64.b64encode(data.getvalue())
            # data64 = base64.b64encode(data)
            hh["src"] = "data:img/jpeg;base64," + data64.decode("utf-8")
            hh["alt"] = round(h.distance, 2)
            hh["name"] = name
            hh["img_url"] = img_url
            hh["score"] = h.distance
            print("MAP:" + name)
            img_id = redis.get("MAP:" + str(name))
            print("IMG:" + img_id)
            hh["metadata"] = redis.json().get("IMG:" + img_id)
            print("image return")
            print(hh["metadata"])
            hit_list.append(hh)
    return hit_list, latency


def predict():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        print("POST:", json_data)

        # Step 2: Access the model prediction function (also validates data)
        result, latency = make_predictions(input_data=json_data)
        # Step 3: Handle errors
        # errors = result.get("errors")
        # if errors:
        #     return Response(json.dumps(errors), status=400)
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
        PREDICTION_LATENCY.labels(
            app_name=APP_NAME, model_name="Clip", model_version="0.1.0"
        ).observe(latency)
        LATENCY_GAUGE.labels(
            app_name=APP_NAME, model_name="Clip", model_version="0.1.0"
        ).set(latency)

        persistence = PredictionPersistence(db_session=flask.g.db_session)
        persistence.save_predictions(
            inputs=json_data,
            model_version="0.1.0",
            predictions=result,
            db_model=ModelType.ClipModel,
        )
        # Step 5: Prepare prediction response
        return jsonify(
            {"predictions": result, "version": "0.1.1", "errors": []}
        )


def feedback():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()
        print("feedback POST:", json_data)
        # TODO: Record this to prometheus
        return jsonify(success=True)
