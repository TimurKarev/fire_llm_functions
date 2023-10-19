# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from firebase_admin import initialize_app, storage
from firebase_functions import https_fn

from lib import files, qdrant_db, embeddings

app = initialize_app()


@https_fn.on_request(timeout_sec=1200)
def get_text_from_pdf_on_request(req: https_fn.Request) -> https_fn.Response:
    path = req.args.get("path")
    name = req.args.get("name")
    if path is None:
        return https_fn.Response("Missing path parameter", 400)
    if name is None:
        return https_fn.Response("Missing name parameter", 400)

    pdf_file = files.get_file_from_firestore(bucket=storage.bucket(), path=path)
    text = files.get_text_from_pdf_file(pdf_file)
    chunks = files.plain_text_separator(text)
    embedding_instruct, collection_size = embeddings.get_instruct_embedding()

    qdrant_db.get_or_create_collection(name=name,
                                       collection_size=collection_size
                                       )

    vector_store = qdrant_db.get_vector_store(
        embeddings=embedding_instruct,
        collection_name=name,
    )

    vector_store.add_texts(chunks)

    return https_fn.Response("True")
