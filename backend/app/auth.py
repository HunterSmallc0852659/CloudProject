import flask
from authlib.integrations.flask_client import OAuth
import os

oauth = OAuth()
auth_bp = flask.Blueprint("auth", __name__)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid email profile https://www.googleapis.com/auth/drive.file"},
)

@auth_bp.route("/login")
def login():
    return google.authorize_redirect(flask.url_for("auth.auth_callback", _external=True))

@auth_bp.route("/callback")
def auth_callback():
    token = google.authorize_access_token()
    flask.session["token"] = token
    return flask.redirect(flask.url_for("routes.upload_file"))
