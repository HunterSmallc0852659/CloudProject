from flask import Flask
from config import Config
from routes import api
from auth import oauth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize OAuth and Routes
    oauth.init_app(app)
    api.init_app(app)

    return app
