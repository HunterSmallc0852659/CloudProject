import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from cleancloud_app import create_app
from unittest.mock import MagicMock, patch
from cleancloud_app.drive_service import upload_file_to_drive



@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_ping(client):
    res = client.get('/ping')
    assert res.status_code == 200
    assert res.json == {"message": "pong"}

@patch("cleancloud_app.drive_service.save_file_metadata")
def test_upload_file_to_drive(mock_save_metadata):
    # Mock drive_service and its files().create().execute() chain
    mock_drive_service = MagicMock()
    mock_file_create = mock_drive_service.files.return_value.create
    mock_file_create.return_value.execute.return_value = {
        "id": "abc123",
        "name": "testfile.txt",
        "mimeType": "text/plain",
        "createdTime": "2025-04-14T12:00:00.000Z"
    }

    # Call function with test values
    file_path = "tests/sample_files/testfile.txt"
    file_name = "testfile.txt"
    mime_type = "text/plain"

    # Run the function
    metadata = upload_file_to_drive(mock_drive_service, file_path, file_name, mime_type)

    # Assert metadata returned correctly
    assert metadata["file_id"] == "abc123"
    assert metadata["file_name"] == "testfile.txt"
    assert metadata["mime_type"] == "text/plain"
    assert metadata["upload_date"] == "2025-04-14T12:00:00.000Z"

    # Assert save_file_metadata was called with correct data
    mock_save_metadata.assert_called_once_with(metadata)

