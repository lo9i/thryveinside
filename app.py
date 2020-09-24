import os

import logging


def init_logging(log_level=None):
    if not log_level:
        log_level = os.environ.get("LOG_LEVEL", "INFO")

    root = logging.getLogger()
    root.setLevel(log_level)


def register_all_modules(flask_app):

    with flask_app.app_context():
        from modules.health import health as health_blueprint
        flask_app.register_blueprint(health_blueprint, url_prefix='/')
        from modules.landing import landing as landing_blueprint
        flask_app.register_blueprint(landing_blueprint, url_prefix='/')
        from modules.foods import foods as foods_blueprint
        flask_app.register_blueprint(foods_blueprint, url_prefix='/foods/')


def create_app():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    flask_app = Flask(__name__)
    flask_app.config.from_object("config.AppConfig")

    the_db = SQLAlchemy()
    the_db.init_app(flask_app)
    return flask_app, the_db


init_logging()
app, db = create_app()
register_all_modules(app)
