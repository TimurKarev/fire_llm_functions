# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from firebase_admin import initialize_app, storage
from firebase_functions import https_fn

from lib import files, qdrant_db, embeddings, retriver
from lib.variables import EmbeddingTypeSized

app = initialize_app()

embedding_type = EmbeddingTypeSized.OPEN_AI


@https_fn.on_request()
def store_document_to_vector_db(req: https_fn.Request) -> https_fn.Response:
    path = req.args.get("path")
    name = req.args.get("collectionName")
    if path is None:
        return https_fn.Response("Missing path parameter", 400)
    if name is None:
        return https_fn.Response("Missing name parameter", 400)

    pdf_file = files.get_file_from_firestore(bucket=storage.bucket(), path=path)
    text = files.get_text_from_pdf_file(pdf_file)
    chunks = files.plain_text_separator(text)
    embedding_instruct = embeddings.get_embedding(type=embedding_type)

    qdrant_db.get_or_create_collection(name=name,
                                       collection_size=embedding_type
                                       )

    vector_store = qdrant_db.get_vector_store(
        embeddings=embedding_instruct,
        collection_name=name,
    )

    vector_store.add_texts(chunks)

    return https_fn.Response("True")


@https_fn.on_request()
def ask_question(req: https_fn.Request) -> https_fn.Response:
    collection_name = req.args.get("collection_name")
    user_id = req.args.get("user_id")
    query = req.args.get("query")
    if collection_name is None:
        return https_fn.Response("Missing collection_name parameter", 400)
    if user_id is None:
        return https_fn.Response("Missing user_id parameter", 400)
    if query is None:
        return https_fn.Response("Missing query parameter", 400)

    embedding = embeddings.get_embedding(type=embedding_type)
    qdrant_db.get_or_create_collection(name=collection_name,
                                       collection_size=embedding_type
                                       )
    context_vector_store = qdrant_db.get_vector_store(
        embeddings=embedding,
        collection_name=collection_name,
    )

    # rag_chain = retriver.get_rag_chain(
    #     context_vector_store
    # )
    #
    # response = rag_chain.invoke(query)

    response = retriver.get_retriever_chain(context_vector_store).run(query)

    return https_fn.Response(response)
