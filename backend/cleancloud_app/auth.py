import os

import flask
from flask import Blueprint
from authlib.integrations.flask_client import OAuth

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

auth_bp = Blueprint("auth", __name__)

oauth = OAuth()

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


# The scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Path to the credentials file
CLIENT_SECRET_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'


def get_drive_service():
    """Authenticate and return a Google Drive service."""
    creds = None

    # Check if we already have valid credentials in token.pickle
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)
    return service