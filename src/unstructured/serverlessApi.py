# Quickstart for using Serverless API    
# https://docs.unstructured.io/api-reference/api-services/saas-api-development-guide

import time
from icecream import ic
import os
import json
import base64
import io
from io import BytesIO


import asyncio


from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig

import logging
logging.basicConfig(level=logging.INFO)


from helperz import analyzeElementsInDirectory,getTablesDataBase64, saveTablesToTablesFolderLocally,\
runPipeline, getSummarizeChainForTextsAndTables, getSummarizeChainForImages, getTablesHtml, getImagesDataBase64, \
save_image_to_folder, saveImagesToImagesFolderLocally, create_folder_if_not_exists, createChromaVectorStore,\
addDocsToVectorstore


from langchain_chroma import Chroma
from langchain_core.stores import InMemoryStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import MultiVectorRetriever
import uuid

import chromadb

from pprint import pprint
from PIL import Image

from dotenv import load_dotenv
load_dotenv()  # Load the .env file


current_file_name = os.path.basename(__file__)
dir_name = os.path.dirname(os.path.basename(__file__))
current_file_directory = os.path.dirname(__file__)
ic(current_file_name)
ic(current_file_directory)


folder_in_path = os.path.join(current_file_directory, "folder_in/attention/") ## folder with all our pdfs
folder_out_path = os.path.join(current_file_directory, "folder_out/attention/") 

def runPipelineMain():
    runPipeline(folder_in_path=folder_in_path, folder_out_path=folder_out_path)



def main_func():



    # Step 1 - run pipeline and perform partitioning/chunking
    



    # Step 2 - analyzing elements -> basically creating 3 arrays (images, tables, texts)

    '''

    analysis = analyzeElementsInDirectory(out_directory_path=folder_out_path)
    
    tables = analysis["tables"]
    images = analysis["images"]
    texts = analysis["texts"]

    ic(len(tables))
    ic(len(images))
    ic(len(texts))

    time.sleep(3)



    # Step 3 - Creating Summarizing Chain for texts, tables, and images
    # we are using the same chain for texts and tables, but different one for images
    summarize_chain_for_texts_and_tables = getSummarizeChainForTextsAndTables()
    summarize_chain_for_images = getSummarizeChainForImages()
    

    

    
    # TEXTS
    text_summaries = summarize_chain_for_texts_and_tables.batch(texts, {"max_concurrency": 3})
    

    pprint(len(text_summaries))
    pprint(len(texts))

    pprint(text_summaries)

    time.sleep(10)





    # TABLES
    tables_html = getTablesHtml(tables=tables)
    table_summaries = summarize_chain_for_texts_and_tables.batch(tables_html, {"max_concurrency": 3})
    

    #storing tables into tables folder - for visual effect here
    
    tablesBase64 = getTablesDataBase64(tables=tables)
    tablesFolder = create_folder_if_not_exists(folder_path=os.path.join(folder_out_path, "tables"))
    saveTablesToTablesFolderLocally(tablesBase64=tablesBase64, folder_path=tablesFolder)
    
    # IMAGES
    

    imagesBase64 = getImagesDataBase64(images=images)
    imagesFolder = create_folder_if_not_exists(folder_path=os.path.join(folder_out_path, "images"))
    saveImagesToImagesFolderLocally(imagesBase64=imagesBase64, folder_path=imagesFolder)
    image_summaries = summarize_chain_for_images.batch(imagesBase64)
    

    # here we have image_summaries, texts_summaries and table_summaries
    # create vectorstore
    ic("Now we will create chroma vectorstore")
    time.sleep(2)

    chroma_persist_directory = os.path.join(folder_out_path, "vectorstore")

    # The vectorstore to use to index the child chunks
    #vectorstore = Chroma(collection_name="attention", embedding_function=OpenAIEmbeddings(), persist_directory=chroma_persist_directory)
    vectorstore = createChromaVectorStore(collection_name="attention", embedding_function=OpenAIEmbeddings(), persist_directory=chroma_persist_directory)

    # The storage layer for the parent documents
    store = InMemoryStore()
    id_key = "doc_id"

    # The retriever (empty to start)
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )



    ic("adding images to chroma")
    numIm = addDocsToVectorstore(retriever=retriever, elements=images, summaries=image_summaries, id_key=id_key)
    ic(numIm)

    ic("adding tables to chroma")
    numTbls=  addDocsToVectorstore(retriever=retriever, elements=tables, summaries=table_summaries, id_key=id_key)
    ic(numTbls)

    ic("adding texts to chroma")
    numTexts = addDocsToVectorstore(retriever=retriever, elements=texts, summaries=text_summaries, id_key=id_key)
    ic(numTexts)

    

    

    

    ic(" - - - - - - Check Retrieval - - - - - -")
    time.sleep(5)

    # Retrieve
    docs = retriever.invoke(
        "What is multihead attention?"
    )

    for doc in docs:
        pprint(doc)
        print("##" * 80)


'''




if __name__== "__main__":

    ic(f"main in ${current_file_name}")
    ''' modified example to create chunks similar to that one in Alejandro's Cohort - Lesson9
    https://colab.research.google.com/drive/1J2gB2fsel8AFgJ-iWuymLYDfWMHx6fer#scrollTo=ipVf219IJX8i
    '''

    runPipelineMain()

    analysis = analyzeElementsInDirectory(out_directory_path=folder_out_path)
    
    # ic(analysis["tables"])
    # ic(analysis["texts"])
    # ic(analysis["images"])

   
    








