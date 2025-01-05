from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

import os
from icecream import ic
from pprint import pprint
import chromadb


from uuid import uuid4
from langchain_core.documents import Document

current_file_name = os.path.basename(__file__)
dir_name = os.path.dirname(os.path.basename(__file__))
current_file_directory = os.path.dirname(__file__)
ic(current_file_directory)
fileName = os.path.join(current_file_directory, "testNba.txt")
ic(fileName)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

chromaPath = os.path.join(current_file_directory, "chroma_1.db")
collectionName = "myTestCollection"

vector_store = Chroma(
    collection_name=collectionName,
    embedding_function=embeddings,
    persist_directory=chromaPath,  # Where to save data locally, remove if not necessary
)

'''

# Initialize from client
persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection("collection_name")
collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

vector_store_from_client = Chroma(
    client=persistent_client,
    collection_name="collection_name",
    embedding_function=embeddings,
)
'''



document_1 = Document(
    page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
    id=1,
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
    id=2,
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
    id=3,
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
    id=4,
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
    id=5,
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
    id=6,
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
    id=7,
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
    id=8,
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news"},
    id=9,
)

document_10 = Document(
    page_content="I have a bad feeling I am going to get deleted :(",
    metadata={"source": "tweet"},
    id=10,
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]

uuids = [str(uuid4()) for _ in range(len(documents))]
ids = vector_store.add_documents(documents=documents, ids=uuids)
ic(ids)



ic(documents)




results = vector_store.similarity_search_by_vector(
    embedding=embeddings.embed_query("Brad pitt ruls"), k=1
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")