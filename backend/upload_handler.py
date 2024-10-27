import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request

app = Flask(__name__)
# Use the connection string directly)
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("BLOB_CONNECTION_STRING"))


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    blob_client = blob_service_client.get_blob_client(container="betslips", blob=file.filename)
    blob_client.upload_blob(file)
    return "Upload successful", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
