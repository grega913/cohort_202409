
from icecream import ic

import uuid
from uuid import uuid4

from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import LocalFileStore
import os


ic(" - - - - - - - VECTORSTORE - - - - - - - -")
current_file_directory = os.path.dirname(__file__)
chromaPath = os.path.join(current_file_directory, "chroma_1.db")

vectorstore = Chroma(
    collection_name="multi_modal_rag",
    embedding_function=OpenAIEmbeddings(),
    persist_directory=chromaPath)


# The storage layer for the parent documents
store = InMemoryStore()
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)

docs = retriever.invoke("What is positional encoding?")

for doc in docs:
    print(str(doc) + "\n\n" + "-" * 80)