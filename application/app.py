from flask import Flask

from .extensions import flask_db
from .configuration import config

app = Flask(__name__)


def create_app(config_name):
    """Creates the app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    configure_extensions(app)
    configure_blueprints(app)

    return app


def configure_extensions(app):
    """Configures the extensions."""

    flask_db.init_app(app)


def configure_blueprints(app):
    from .home import bp_home
    app.register_blueprint(bp_home, url_prefix='/home')

    from .search import bp_search
    app.register_blueprint(bp_search, url_prefix='/search')

    from .statistics import bp_statistics
    app.register_blueprint(bp_statistics, url_prefix='/statistics')

    from .download import bp_download
    app.register_blueprint(bp_download, url_prefix='/download')

    from .publications import bp_publications
    app.register_blueprint(bp_publications, url_prefix='/publications')
