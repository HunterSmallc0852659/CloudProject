from flask_pymongo import PyMongo
from pymongo import MongoClient
from .__init__ import create_app


client = MongoClient('mongodb://localhost:27017/')
db = client['CloudProjectDB']
collection = db['CloudProjectCollection']

app = create_app()
mongo = PyMongo(app)

class MyModel(object):
    def __init__(self, data):
        self.data = data

    def save(self):
        collection.insert_one(self.data)

def save_file_metadata(file_metadata):
    """ Save metadata to MongoDB """
    mongo.db.files.insert_one(file_metadata)

def get_files():
    """ Retrieve all stored metadata """
    return list(mongo.db.files.find({}, {"_id": 0}))
