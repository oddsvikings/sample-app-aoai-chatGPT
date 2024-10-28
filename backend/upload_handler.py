
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, ContentSettings
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Azure Blob Storage configuration
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_name = "betslips"

# Allowed image file extensions for validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # Check if the file has a valid image extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Save the file to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        
        # Optionally process or analyze the image here
        # Example: Call a function to analyze the image (e.g., OCR or image classification)

        # Upload with content settings for image type
        content_settings = ContentSettings(content_type=file.content_type)
        blob_client.upload_blob(file, content_settings=content_settings, overwrite=True)

        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "Invalid file type. Only images are allowed."}), 400
