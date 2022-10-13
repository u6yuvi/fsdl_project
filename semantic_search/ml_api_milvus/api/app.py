import logging

import connexion
import flask
import redis
from flask_cors import CORS
from ml_api_milvus.api.config import Config
from ml_api_milvus.api.persistence.core import init_database
from ml_api_milvus.api.monitoring.middleware import setup_metrics
from pymilvus import Collection, connections
from sentence_transformers import SentenceTransformer

_logger = logging.getLogger(__name__)


def load_corpus():
    connections.connect("default", host="34.168.23.74", port="19530")
    # TODO test if connexion exists
    # collection_ip = "fsdl_cosine"
    collection_ip = "fsdl_ip"
    fsdl_ip = Collection(collection_ip)
    _logger.info(fsdl_ip)
    fsdl_ip.load()
    _logger.info(collection_ip + " loaded.")
    return fsdl_ip


def load_model():
    img_model = SentenceTransformer("clip-ViT-B-32")
    return img_model


def create_app(*, config_object: Config) -> connexion.App:
    """Create app instance."""

    connexion_app = connexion.App(
        __name__, debug=config_object.DEBUG, specification_dir="spec/"
    )
    flask_app = connexion_app.app
    flask_app.config.from_object(config_object)
    CORS(flask_app)

    # Setup database
    db_session = init_database(flask_app, config=config_object)

    # Setup prometheus monitoring
    setup_metrics(flask_app)

    connexion_app.add_api("api.yaml")
    # make the flak app the current context so we could share the corpus
    flask_app.app_context().push()

    # the api server will serve the images from here
    fsdl_ip = load_corpus()
    flask.g.fsdl_ip = fsdl_ip

    model = load_model()
    flask.g.model = model

    #postgreSQL 
    flask.g.db_session = db_session

    flask.g.redis = redis.Redis(
        host=config_object.REDIS_HOST,
        port=config_object.REDIS_PORT,
        password=config_object.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )

    _logger.info("Application instance created")

    return connexion_app
