from flask_pymongo import PyMongo
from app import create_app

app = create_app()
mongo = PyMongo(app)

def save_file_metadata(file_metadata):
    """ Save metadata to MongoDB """
    mongo.db.files.insert_one(file_metadata)

def get_files():
    """ Retrieve all stored metadata """
    return list(mongo.db.files.find({}, {"_id": 0}))
