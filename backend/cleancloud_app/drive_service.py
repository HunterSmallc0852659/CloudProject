from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from .shared import save_file_metadata

def upload_file_to_drive(drive_service, file_path, file_name, mime_type):
    """Uploads a file to Google Drive and saves metadata in MongoDB."""
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
    # save_file_metadata() function implementation is not shown in the code snippet
    save_file_metadata(file_metadata)

    return file_metadata