from flask import Flask
from app.config import Config
from app.routes import api
from app.auth import oauth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize OAuth and Routes
    oauth.init_app(app)
    api.init_app(app)

    return app
