from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os

# MongoDB URI from .env or configuration file
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Replace with your actual URI
client = MongoClient(MONGO_URI)

# Database and collection setup
db = client["CloudProject_db"]
collection = db["files"]

def save_file_metadata(file_metadata):
    """Saves the metadata to MongoDB."""
    # Ensure the upload_date is in the correct format (ISO 8601)
    if isinstance(file_metadata["upload_date"], str):
        file_metadata["upload_date"] = datetime.strptime(file_metadata["upload_date"], "%Y-%m-%dT%H:%M:%SZ")

    # Insert into the database
    result = collection.insert_one(file_metadata)
    return result.inserted_id  # Returns the _id of the inserted document

# Example file metadata
file_metadata = {
    "file_id": "1ABCDefgHIJKLmnoPQRstUV",
    "file_name": "resume.pdf",
    "mime_type": "application/pdf",
    "upload_date": "2025-04-14T15:23:00Z"
}

# Save the file metadata
inserted_id = save_file_metadata(file_metadata)
print(f"Inserted document ID: {inserted_id}")
