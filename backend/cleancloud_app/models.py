from flask_pymongo import PyMongo

# Use the mongo instance from PyMongo initialized in create_app()
mongo = PyMongo()

class MyModel(object):
    def __init__(self, data):
        self.data = data

    def save(self):
        """ Save data to MongoDB """
        mongo.db.CloudProjectCollection.insert_one(self.data)  # Using the PyMongo instance

def get_files():
    """ Retrieve files from MongoDB """
    try:
        files = mongo.db.CloudProjectCollection.find()  # Use PyMongo to access the collection
        return [file for file in files]
    except Exception as e:
        raise Exception(f"Error fetching files: {str(e)}")
