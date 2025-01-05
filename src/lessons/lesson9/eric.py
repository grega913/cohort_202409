
# from the canadian guy https://www.youtube.com/watch?v=KQAz7KqCHJw&ab_channel=EricVaillancourt
# https://medium.com/@eric_vaillancourt/enough-with-prototyping-time-for-persistent-multi-vector-storage-with-postgresql-in-langchain-8e678738e80d

import sqlite3
import os
from icecream import ic
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.storage import SQLStore
import time
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.document_loaders import PyPDFLoader
from database import COLLECTION_NAME, CONNECTION_STRING
from store import PostgresByteStore
from langchain_postgres import PGVector
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter


from dotenv import load_dotenv
load_dotenv()


from dotenv import load_dotenv


# Load environment variables
load_dotenv()



def getDocs(fname="montreal.pdf"):
    ic("def getDocs")

    current_file_directory = os.path.dirname(__file__)
    montrealDocPath = os.path.join(current_file_directory, "data", fname)

    loader = PyPDFLoader(file_path=montrealDocPath)

    # by default, we will split by pages with no text_splitter
    documents = loader.load_and_split(text_splitter=None)
    return documents



def getDocIds(documents):
    return [str(uuid.uuid4()) for _ in documents]


def splitDocs(documents):
    ic("def splitDocs")

    child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

    doc_ids = getDocIds(documents=documents)

    ic(doc_ids)

    id_key="doc_id"

    all_sub_docs = []
    for i, doc in enumerate(documents):
        doc_id = doc_ids[i]
        sub_docs = child_text_splitter.split_documents([doc])
        for sub_doc in sub_docs:
            sub_doc.metadata[id_key] = doc_id
        all_sub_docs.extend(sub_docs)
        
    return all_sub_docs






def simpleMultiVectorRetriever():
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings()
    )

    store = InMemoryStore()

    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore, 
        docstore=store, 
        id_key=id_key,
    )

    return retriever



def postgresMultiVectorRetriever():

    embeddings = OpenAIEmbeddings()
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

    store = PostgresByteStore(CONNECTION_STRING, COLLECTION_NAME)
    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore, 
        docstore=store, 
        id_key=id_key,
    )

    return retriever


if __name__=="__main__":

    retriever = postgresMultiVectorRetriever()
    ic(retriever)

    documents = getDocs(fname="attention.pdf")
    ic(documents)

    all_sub_docs = splitDocs(documents=documents)
    ic(all_sub_docs)

    doc_ids = getDocIds(documents=documents)

    retriever.vectorstore.add_documents(all_sub_docs)

    filename = "montreal.pdf"

    retriever.docstore.mset(list(zip(doc_ids, documents, filename)))






    time.sleep(10)

    #retriever = simpleMultiVectorRetriever()
    #ic(retriever)




