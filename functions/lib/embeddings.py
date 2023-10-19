from typing import Tuple

from langchain.embeddings import HuggingFaceInstructEmbeddings

from .variables import EmbendingSize


def get_instruct_embedding() -> Tuple[HuggingFaceInstructEmbeddings, int]:
    return (HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl"),
            EmbendingSize.INSTRUCTOR
            )
