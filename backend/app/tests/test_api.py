import os
import pytest
from app import create_app
from app.models import mongo


# Set up the Flask app for testing
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'

    # Create test database (if needed)
    with app.app_context():
        mongo.db.create_collection('files')  # You can skip this if it's not necessary for your tests

    yield app

    # Clean up test database
    with app.app_context():
        mongo.db.drop_collection('files')


# Set up a test client for sending HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()


# Test for uploading a file
def test_upload_file(client):
    # Sample file content (can use a small image or any file for testing)
    data = {
        'file': (open('sample.txt', 'rb'), 'sample.txt')  # Path to an actual file for testing
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data


# Test for getting file metadata
def test_get_files(client):
    response = client.get('/files')

    assert response.status_code == 200
    assert b"files" in response.data
