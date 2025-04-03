from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from flask import session
from app.models import save_file_metadata
import os


def get_drive_service():
    """Authenticate and return Google Drive service instance."""
    credentials = session.get("token")
    if not credentials:
        raise Exception("User not authenticated")

    return build("drive", "v3", credentials=credentials)


def upload_file_to_drive(file_path, file_name, mime_type):
    """Uploads a file to Google Drive and saves metadata in MongoDB."""
    drive_service = get_drive_service()

    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = drive_service.files().create(body=file_metadata, media_body=media,
                                        fields="id, name, mimeType, createdTime").execute()

    # Save metadata in MongoDB
    file_metadata = {
        "file_id": file.get("id"),
        "file_name": file.get("name"),
        "mime_type": file.get("mimeType"),
        "upload_date": file.get("createdTime"),
    }
    save_file_metadata(file_metadata)

    return file_metadata
