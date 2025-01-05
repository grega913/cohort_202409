# this version is using postgres db for docstore - instead of in MemoryStore


import os
import sys
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
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


from l9_multimodal_RAG import make_chunks, get_images_base64

from l9_prompts import PROMPT_TEXT, PROMPT_TEMPLATE

data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(data_dir)

tables = []
texts = []

if __name__ == "__main__":
    ic("def name = main in l9_multimodal_RAG_pg")
    
    data_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(data_dir, "data", "attention.pdf")
    output_path = os.path.join(data_dir, "output")

    chunksFilePath = os.path.join(output_path, "att.json")

    persistence_directory = os.path.join(data_dir, "vectorstore")

    
    ic(data_dir)
    ic(file_path)
    ic(output_path)
    ic(persistence_directory)



    chunks = make_chunks(file_path=file_path, output_path=output_path)
    

    ic("here we should have chunks")
    ic(len(chunks))



    for chunk in chunks:
        ic(str(type(chunk)))

    ic("fill tables and texts")
    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk)
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk)
    
    ic("fill images")
    images = get_images_base64(texts)

    ic(len(texts))
    ic(len(tables))
    ic(len(images))

    time.sleep(8)



    # Prompt
    prompt_text = """
        You are an assistant tasked with summarizing tables and text.
        Give a concise summary of the table or text.

        Respond only with the summary, no additionnal comment.
        Do not start your message by saying "Here is a summary" or anything like that.
        Just give the summary as it is.

        Table or text chunk: {element}

        """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Summary chain
    model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Summarize text
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

    # Summarize tables
    tables_html = [table.metadata.text_as_html for table in tables]
    table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})



    prompt_template = """Describe the image in detail. For context,
                    the image is part of a research paper explaining the transformers
                    architecture. Be specific about graphs, such as bar plots."""
    messages = [
        (
            "user",
            [
                {"type": "text", "text": prompt_template},
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image}"},
                },
            ],
        )
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

    image_summaries = chain.batch(images)



    ic(" - - - - - SUMMARIES - - - - - - -")

    ic(text_summaries)
    ic(table_summaries)
    ic(image_summaries)

    ic(" - - - - - - END OF SUMMARIES - - - - - -")


    # The vectorstore to use to index the child chunks
    # vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=OpenAIEmbeddings())

    ic(" - - - - - - - VECTORSTORE - - - - - - - -")
    current_file_directory = os.path.dirname(__file__)
    chromaPath = os.path.join(current_file_directory, "my_chroma")

    '''
    vectorstore = Chroma(
        collection_name="multi_modal_rag",
        embedding_function=OpenAIEmbeddings(),
        persist_directory=chromaPath
    )
    '''

    embeddings = OpenAIEmbeddings()
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )



    # The storage layer for the parent documents
    #store = InMemoryStore() # the original version, where store is inMemory
    
    #define store ads PostgresByteSore - - of course make sure that postgres is running
    store = PostgresByteStore(CONNECTION_STRING, COLLECTION_NAME)
    id_key = "doc_id"
    ic("here we should be defining our retriever")

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key
    )
    ic(retriever)
    time.sleep(10)


    filename = "attention.pdf"

    # Add texts
    ic("adding texts")
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=summary, metadata={id_key: doc_ids[i]}) for i, summary in enumerate(text_summaries)
    ]
    retriever.vectorstore.add_documents(summary_texts)
    
    retriever.docstore.mset(list(zip(doc_ids, texts, filename)))

    # Add tables
    ic("adding tables")
    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_tables = [
        Document(page_content=summary, metadata={id_key: table_ids[i]}) for i, summary in enumerate(table_summaries)
    ]
    retriever.vectorstore.add_documents(summary_tables)
    retriever.docstore.mset(list(zip(table_ids, tables, filename)))

    # Add image summaries
    ic("adding images")
    img_ids = [str(uuid.uuid4()) for _ in images]
    summary_img = [
        Document(page_content=summary, metadata={id_key: img_ids[i]}) for i, summary in enumerate(image_summaries)
    ]
    retriever.vectorstore.add_documents(summary_img)
    retriever.docstore.mset(list(zip(img_ids, images, filename)))

    time.sleep(20)


    ic(" - - - - - - - - CHECK RETRIEVER - - - - - - - ")
    # Retrieve

    question = "What is in Table 3?"
    ic(question)
    docs = retriever.invoke(question)

    ic(len(docs))
    
    for doc in docs:
        print(str(doc) + "\n\n" + "-" * 80)
