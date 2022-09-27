import prometheus_client
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import sys
import os
print(os.getcwd())
sys.path.append("/home/uv/Documents/backup/Documents/github/fsdl_project/semantic_search/ml_api/api")
print(sys.path)
from ml_api.api.app import create_app
from ml_api.api.config import DevelopmentConfig, setup_app_logging
from werkzeug.serving import run_simple


_config = DevelopmentConfig()

# setup logging as early as possible
setup_app_logging(config=_config)

main_app = create_app(config_object=_config).app
application = DispatcherMiddleware(
        app=main_app.wsgi_app,
        mounts={'/metrics': prometheus_client.make_wsgi_app()}
    )


if __name__ == "__main__":
    run_simple(port=_config.SERVER_PORT, hostname=_config.SERVER_HOST,application = application)