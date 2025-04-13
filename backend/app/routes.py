from flask import Blueprint, request
from flask_restful import Api, Resource

from drive_service import upload_file_to_drive

routes_bp = Blueprint("routes", __name__)
api = Api(routes_bp)


class UploadFile(Resource):
    def post(self):
        """ Handle file upload request """
        if "file" not in request.files:
            return {"error": "No file provided"}, 400

        file = request.files["file"]
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        try:
            metadata = upload_file_to_drive(file_path, file.filename, file.mimetype)
            return {"message": "File uploaded successfully", "metadata": metadata}, 200
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(UploadFile, "/upload")
