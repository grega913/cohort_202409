
import os
import json

import json, base64

import os
import base64
from PIL import Image
import io
from io import BytesIO

import uuid

from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
    LocalUploaderConfig
)
from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from icecream import ic
import time

from dotenv import load_dotenv
load_dotenv()  # Load the .env file

api_key = os.getenv("UNSTRUCTURED_API_KEY")
api_url= os.getenv("UNSTRUCTURED_API_URL")



def runPipeline(folder_in_path: str, folder_out_path):
        Pipeline.from_configs(
        context=ProcessorConfig(),
        indexer_config=LocalIndexerConfig(input_path=folder_in_path),
        downloader_config=LocalDownloaderConfig(),
        source_connection_config=LocalConnectionConfig(),
        partitioner_config=PartitionerConfig(
            strategy="hi_res",
            api_key=api_key,
            partition_endpoint=api_url,
            infer_table_structure=True,
            extract_image_block_types=["Image"],
            extract_image_block_output_dir=folder_out_path,
            extract_image_block_to_payload=True,
            additional_partition_args={
                "split_pdf_page": True,
                "split_pdf_allow_failed": True,
                "split_pdf_concurrency_level": 15
            }
            ),
        chunker_config=ChunkerConfig(
            chunking_strategy="by_title",
            chunk_max_characters=10000,
            chunk_combine_text_under_n_chars=2000,
            chunk_new_after_n_chars=6000
            ),
        uploader_config=LocalUploaderConfig(output_dir=folder_out_path)
        ).run()

def analyzeElementsInDirectory(out_directory_path: str):
    ic(f"analyzeElementsInDirectory: ${out_directory_path}")
    
    total_elements = 0
    total_images = 0
    type_counts = {}
    tables = [] 
    images = [] 
    texts = []


    for filename in os.listdir(out_directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(out_directory_path, filename)
            with open(file_path, 'r') as file:
                ic(f"file_path: ${file_path}")
                file_elements = json.load(file)

            imageCount = 0
            for element in file_elements: 
                element_type = element['type']
                elementMetadata = element['metadata']
                # ic(elementMetadata)

                if element_type in type_counts:
                    type_counts[element_type] += 1
                else:
                    type_counts[element_type] = 1
                '''
                if "image_base64" in elementMetadata:
                    ic("we have image_data here")

                    image_data = base64.b64decode(elementMetadata["image_base64"])
                    image_name = f"image_{imageCount}.jpg" 

                    images_folder = os.path.join(os.path.dirname(file_path), "blocks")  
                    if not os.path.exists(images_folder):  
                        os.makedirs(images_folder)

                    with open(os.path.join(images_folder, image_name), 'wb') as f:
                        f.write(image_data)  # Write the image data to a file

                    imageCount += 1
                    total_images += 1
                '''
                if element_type=="Table":
                    ic("append to tables")
                    tables.append(element)
                elif element_type=="Image":
                    ic("append to images")
                    images.append(element)
                elif (element_type !="Table" and element_type !="Image"):
                    ic("appending to texts")
                    texts.append(element)

            total_elements += len(file_elements)

    return {
        "tables": tables,
        "images": images,
        "texts": texts
        }

def getSummarizeChainForTextsAndTables():
    ic("getSummarizeChain")

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
    # model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant")
    model = ChatOpenAI(model="gpt-4o-mini")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    return summarize_chain

def getTablesHtml(tables):
    tables_html=[] # this will go into summarize_chain
    for table in tables:
        tblData = table["metadata"]["text_as_html"]
        tables_html.append(tblData)
    
    return tables_html

def getImagesDataBase64(images):
    ic("def getImagesDataBase64")
    images_b64=[]
    for image in images:
        imgData = image["metadata"]["image_base64"]
        images_b64.append(imgData)
    return images_b64

def getTablesDataBase64(tables):
    ic("def getTablesDataBase64")
    tables_b64=[]
    for table in tables:
        tblData = table["metadata"]["image_base64"]
        tables_b64.append(tblData)
    return tables_b64

def getTablesDataBase64_v2(tables):
    ic("def getTablesDataBase64")
    tables_b64=[]
    for table in tables:
        tblData = table["metadata"]["orig_elements"]
        tables_b64.append(tblData)
    return tables_b64

def saveImagesToImagesFolderLocally(imagesBase64, folder_path):
    i=0
    for imageBase64 in imagesBase64:
        file_path = os.path.join(folder_path, "image_" + str(i) + ".png")
        image_data = base64.b64decode(imageBase64)
        image = Image.open(BytesIO(image_data))
        image.save(file_path)
        i=i+1

def saveTablesToTablesFolderLocally(tablesBase64, folder_path):
    i=0
    for tableBase64 in tablesBase64:
        file_path = os.path.join(folder_path, "table_" + str(i) + ".png")
        table_data = base64.b64decode(tableBase64)
        table = Image.open(BytesIO(table_data))
        table.save(file_path)
        i=i+1

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def save_image_to_folder(base64_code, folder_path, i):
    # Decode the base64 string to binary
    image_data = base64.b64decode(base64_code)
    # Create an image object from the binary data
    image = Image(data=image_data)
    # Display the image
    
    imgPath = folder_path + "image_" + str(i) + ".png"
    image.save(imgPath)

def getSummarizeChainForImages():
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

    summarizeChainForImages = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser() 

    return summarizeChainForImages

def createChromaVectorStore(collection_name: str, embedding_function, persist_directory):
    return Chroma(collection_name= collection_name, embedding_function=embedding_function, persist_directory=persist_directory)


'''
def addDocsToVectorstore(retriever, elements, summaries, id_key):
    ic("async def addDocsToVectorstore")
    ids = [str(uuid.uuid4()) for _ in elements]

    summ = [Document(page_content=summary, metadata={id_key: ids[i]}) for i, summary in enumerate(summaries)]

    ic("before adding documents and summary is")
    ic(summ)

    retriever.vectorstore.add_documents(summ)
    retriever.docstore.mset(list(zip(ids, elements)))

    ic("before return in def addDocsToVectorstore")
    return len(elements)
'''

def addDocsToVectorstore(retriever, elements, summaries, id_key):
    ic("async def addDocsToVectorstore")
    ids = [str(uuid.uuid4()) for _ in elements]

    summ = [Document(page_content=summary, metadata={id_key: ids[i]}) for i, summary in enumerate(summaries)]

    ic("before adding documents and summary is")
    ic(summ)

    batch_size = 20
    for i in range(0, len(summ), batch_size):
        batch_summ = summ[i:i + batch_size]

        ic(len(batch_summ))

        retriever.vectorstore.add_documents(batch_summ)
        retriever.docstore.mset(list(zip([ids[j] for j in range(i, min(i + batch_size, len(summ)))], [elements[j] for j in range(i, min(i + batch_size, len(summ)))])))

    ic("before return in def addDocsToVectorstore")
    return len(elements)



