import pymongo

def save_file_metadata(file_metadata):
    """ Save metadata to MongoDB """
    mongo.db.files.insert_one(file_metadata)