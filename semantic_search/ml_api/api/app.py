import logging

import connexion
from flask_cors import CORS
from ml_api.api.config import Config
from ml_api.api.monitoring.middleware import setup_metrics

_logger = logging.getLogger(__name__)


def create_app(*, config_object: Config) -> connexion.App:
    """Create app instance."""

    connexion_app = connexion.App(
        __name__, debug=config_object.DEBUG, specification_dir="spec/"
    )
    flask_app = connexion_app.app
    flask_app.config.from_object(config_object)
    CORS(flask_app)

    # Setup prometheus monitoring
    setup_metrics(flask_app)

    connexion_app.add_api("api.yaml")

    _logger.info("Application instance created")

    return connexion_app
