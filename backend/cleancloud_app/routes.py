from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from .drive_service import upload_file_to_drive
from .auth import get_drive_service
import os

# Create a blueprint
routes_bp = Blueprint("routes", __name__)
# Attach Flask-RESTful API to the blueprint
api = Api(routes_bp)

# Define a Resource
class UploadFile(Resource):
    def post(self):
        """ Handle file upload request """
        if "file" not in request.files:
            return {"error": "No file provided"}, 400

        file = request.files["file"]
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        try:
            drive_service = get_drive_service()
            metadata = upload_file_to_drive(drive_service, file_path, file.filename, file.mimetype)
            return {"message": "File uploaded successfully", "metadata": metadata}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

def register_routes(app):
    @app.route('/ping')
    def ping():
        return jsonify({'message': 'pong'})

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    drive_service = get_drive_service()
    metadata = upload_file_to_drive(
        drive_service=drive_service,
        file_path=file,
        file_name=file.filename,
        mime_type=file.mimetype
    )
    return jsonify(metadata)

# Register the resource with the API
api.add_resource(UploadFile, "/upload")

from .models import get_files  # make sure this import is placed at the top if not already

@routes_bp.route("/files", methods=["GET"])
def list_files():
    try:
        files = get_files()
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

