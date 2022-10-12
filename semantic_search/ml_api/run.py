import prometheus_client
from ml_api.api.app import create_app
from ml_api.api.config import DevelopmentConfig, setup_app_logging
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

_config = DevelopmentConfig()

# setup logging as early as possible
setup_app_logging(config=_config)

main_app = create_app(config_object=_config).app
application = DispatcherMiddleware(
    app=main_app.wsgi_app,
    mounts={"/metrics": prometheus_client.make_wsgi_app()},
)


if __name__ == "__main__":
    run_simple(
        port=_config.SERVER_PORT,
        hostname=_config.SERVER_HOST,
        application=application,
    )
