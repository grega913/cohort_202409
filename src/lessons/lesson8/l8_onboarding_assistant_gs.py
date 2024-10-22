import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from icecream import ic
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
import faiss

from dotenv import load_dotenv
load_dotenv()  # Load the .env file



# region Create RAG - my solution 20241002


# load docs
def loadDocs():
    ic("loadDocs")

    directory = os.getcwd()
    fPath = os.path.join(directory ,"src/lessons/data", "umbrella_corp_policies.pdf")
    ic(fPath)
    loader = PyPDFLoader(fPath)
    docs = loader.load()
    return docs

# split docs
def splitDocs(docs):
    ic("splitDocs")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits

# store splits into vector database - using Chroma
def storeSplitsIntoVectorDatabase_Chroma(splits):
    ic("storeSplitsIntoVectorDatabase_Chroma")

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever() # Retriever is Runnable
    return retriever

# store splits into vector database - using FAISS
def storeSplitsIntoVectorDatabase_Faiss(splits):
    ic("storeSplitsIntoVectorDatabase_Faiss")


    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    uuids = [str(uuid4()) for _ in range(len(splits))]

    vector_store.add_documents(documents=splits, ids=uuids)

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 1})
    return retriever

# creating RAG chain
def getRAGChain():
    ic("getRAGChain")
    
    llm = ChatGroq(model = "llama-3.1-70b-versatile")
    docs = loadDocs()
    splits = splitDocs(docs=docs)
    retriever = storeSplitsIntoVectorDatabase_Chroma(splits=splits)

    # little helper function for parsing docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt_template = """
        You are an onboarding assistant that answers questions based on the context provided below.

        Context:
        {context}

        Question:
        {question}

        Please provide a detailed and accurate answer based on the given context.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()

    )

    return rag_chain



# endregion



# region Alejandro's Solution from video - https://app.alejandro-ao.com/topics/rag-lab-solution/ - 20241022



# endregion

if __name__== "__main__":
    ic(__name__)
    chain = getRAGChain()
    ic(chain.invoke("What is company's stand on Good Manufacturing Practice (GMP)?"))
