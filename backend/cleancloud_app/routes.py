# routes.py

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from .drive_service import upload_file_to_drive
from .auth import get_drive_service
from .models import get_files  # Import it here
import os

routes_bp = Blueprint("routes", __name__)
api = Api(routes_bp)

@routes_bp.route("/files", methods=["GET"])
def get_files_route():
    try:
        files = get_files()  # Call the function from models.py
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

    # Register the resource with the API
    api.add_resource(UploadFile, "/upload")
    app.register_blueprint(routes_bp, url_prefix="/api")
