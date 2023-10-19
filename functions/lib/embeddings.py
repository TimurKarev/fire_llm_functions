from langchain.embeddings import HuggingFaceInstructEmbeddings
from .variables import EmbendingSize

def embed_text(text: str) -> (HuggingFaceInstructEmbeddings, int):
    return (HuggingFaceInstructEmbeddings(model='hkunlp/instructor-x1'),
            EmbendingSize.INSTRUCTOR
            )