import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.conversions import common_types as types

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API")
)

def get_or_create_collection(name: str, collection_size: int)-> types.CollectionInfo:
    collection = None

    if (name in qdrant_client.get_collections()):
        collection = qdrant_client.get_collection(collection_name=name)
    else:
        collection = qdrant_client.recreate_collection(collection_name=name,
                                                       vectors_config=models.VectorParams(
                                                           size=collection_size,
                                                           distance=models.Distance.COSINE,
                                                       )
               )

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(collection)


    # try:
    #     collection = qdrant_client.get_collection(collection_name=name)
    # except http.exceptions.UnexpectedResponse:
    #
    #     collection = qdrant_client.recreate_collection(name=name)

    return collection
def store_to_db(bucket, path, data):
    pass

