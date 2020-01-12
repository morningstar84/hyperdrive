import os

from flask import Flask

from config import config


def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_ENV')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .hyperdrive import hyperdrive as hype_blueprint
    app.register_blueprint(hype_blueprint, url_prefix='/api/hyperdrive')
    return app
