#https://colab.research.google.com/drive/1J2gB2fsel8AFgJ-iWuymLYDfWMHx6fer#scrollTo=7_qX-vAgHDG-

from dotenv import load_dotenv
load_dotenv()
import os
import sys
import time
import json
import pickle

from icecream import ic
from unstructured.partition.pdf import partition_pdf

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import uuid
from uuid import uuid4

from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.storage import SQLStore

from pprint import pprint



def store_elements_to_file(elements, filename):
    with open(filename, 'wb') as f:
        pickle.dump(elements, f)

from l9_prompts import PROMPT_TEXT, PROMPT_TEMPLATE

data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(data_dir)

tables = []
texts = []


def make_chunks(file_path, output_path):
    ic("def make_chunks")
    chunks = partition_pdf(
        filename=file_path,
        infer_table_structure=True,             # extract Tables
        strategy="hi_res",                      # mandatory to infer tables
        extract_image_block_types=["Image"],
        image_output_dir_path = output_path,    # folder for images to be downloaded, if we want to have it stored locally
        extract_image_block_to_payload=True, # if true, will extract base64 for API usage

        chunking_strategy="by_title", # or 'basic' -> putting elements together
        max_characters=10000,
        combine_text_under_n_chars=2000,
        new_after_n_chars=6000,
    )

    return chunks


# Get the images from CompositeElement objects
def get_images_base64(chunks):
    ic("def get_images_base64")
    images_b64=[]
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)):
                    images_b64.append(el.metadata.image_base64)
    return images_b64



if __name__ == "__main__":
    ic("def name = main in l9_multimodal_RAG")
    
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

    for text in texts:
        ic(text)
        ic(type(text))




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

    
    vectorstore = Chroma(
        collection_name="multi_modal_rag",
        embedding_function=OpenAIEmbeddings(),
        persist_directory=chromaPath
    )



    # The storage layer for the parent documents
    store = InMemoryStore() # the original version, where store is inMemory

    ic("here we should be defining our store")
    
    '''
    sqlitepath = os.path.join(current_file_directory, "sq_test.db")
    db_url="sqlite:///" + str(sqlitepath)

    #db_url="sqlite:///" + str(chromaPath)
    ic(db_url)

    sql_store = SQLStore(namespace="langchain_key_value_stores", db_url=db_url)
    '''



    id_key = "doc_id"

    

    ic("here we should be defining our retriever")

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key
    )

    

    # Add texts
    ic("adding texts")
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=summary, metadata={id_key: doc_ids[i]}) for i, summary in enumerate(text_summaries)
    ]
    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(doc_ids, texts)))

    # Add tables
    ic("adding tables")
    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_tables = [
        Document(page_content=summary, metadata={id_key: table_ids[i]}) for i, summary in enumerate(table_summaries)
    ]
    retriever.vectorstore.add_documents(summary_tables)
    retriever.docstore.mset(list(zip(table_ids, tables)))

    # Add image summaries
    ic("adding images")
    img_ids = [str(uuid.uuid4()) for _ in images]
    summary_img = [
        Document(page_content=summary, metadata={id_key: img_ids[i]}) for i, summary in enumerate(image_summaries)
    ]
    retriever.vectorstore.add_documents(summary_img)
    retriever.docstore.mset(list(zip(img_ids, images)))




    ic(" - - - - - - - - CHECK RETRIEVER - - - - - - - ")
    # Retrieve

    question = "What is in Table 3?"
    ic(question)
    docs = retriever.invoke(question)

    ic(len(docs))
    
    for doc in docs:
        print(str(doc) + "\n\n" + "-" * 80)





