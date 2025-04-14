from flask import Flask
from .config import Config
from .auth import auth_bp

from .routes import routes_bp  # This is the blueprint that includes the Api + Resource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .auth import oauth
    oauth.init_app(app)

    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix="/api")  # ✅ CORRECT
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
