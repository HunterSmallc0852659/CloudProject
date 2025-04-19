from flask import Flask
from .config import Config
from .auth import auth_bp, oauth
from flask_pymongo import PyMongo

# Initialize PyMongo here, no need to use MongoClient separately
mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    # Load configurations from Config class
    app.config.from_object(Config)

    # Initialize OAuth
    oauth.init_app(app)

    # Set Mongo URI for MongoDB
    app.config["MONGO_URI"] = "mongodb://localhost:27017/CloudProjectDB"

    # Initialize MongoDB extension
    mongo.init_app(app)

    # Import routes and register them here to avoid circular imports
    from .routes import register_routes
    register_routes(app)

    # Register auth blueprint
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
