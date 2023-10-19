# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from firebase_functions import https_fn
from firebase_admin import initialize_app, storage
from lib import files, embeddings, qdrant_db

app = initialize_app()


@https_fn.on_request()
def get_text_from_pdf_on_request(req: https_fn.Request) -> https_fn.Response:
    path = req.args.get("path")
    if path is None:
        return https_fn.Response("Missing path parameter", 400)

    pdf_file = files.get_file_from_firestore(bucket=storage.bucket(), path=path)
    text = files.get_text_from_pdf_file(pdf_file)

    collection_size = 768
    collection = qdrant_db.get_or_create_collection(name="test", collection_size=collection_size)

    return https_fn.Response(text)
