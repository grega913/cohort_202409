# Async Partitioning
# https://docs.unstructured.io/api-reference/api-services/sdk-python#async-partitioning

import asyncio
import os
import json
import unstructured_client
from unstructured_client.models import shared
import json, base64, io
from PIL import Image

from icecream import ic
import time
from dotenv import load_dotenv
load_dotenv()  # Load the .env file

from helperz import analyzeElementsInDirectory


client = unstructured_client.UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
    server_url=os.getenv("UNSTRUCTURED_API_URL"),
)



current_file_name = os.path.basename(__file__)
dir_name = os.path.dirname(os.path.basename(__file__))
current_file_directory = os.path.dirname(__file__)
ic(current_file_name)
ic(current_file_directory)




async def call_api(filename, input_dir, output_dir):
    req = {
        "partition_parameters": {
            "files": {
                "content": open(filename, "rb"),
                "file_name": os.path.basename(filename),
            },
            "strategy": shared.Strategy.HI_RES,
            "split_pdf_page":True,
            "split_pdf_allow_failed":True,
            "split_pdf_concurrency_level":10,
            "extract_image_block_types": ["Image"],
            "chunking_strategy": shared.ChunkingStrategy.BY_TITLE,
            "max_characters": 10000,
            "combine_text_under_n_chars":2000,
            "new_after_n_chars":6000
        }
    }

    try:
        res = await client.general.partition_async(request=req)
        element_dicts = [element for element in res.elements]
        json_elements = json.dumps(element_dicts, indent=2)

        # Create the output directory structure.
        relative_path = os.path.relpath(os.path.dirname(filename), input_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        os.makedirs(output_subdir, exist_ok=True)

        # Write the output file.
        output_filename = os.path.join(output_subdir, os.path.basename(filename) + ".json")
        with open(output_filename, "w") as file:
            file.write(json_elements)

    except Exception as e:
        print(f"Error processing {filename}: {e}")

async def process_files(input_directory, output_directory):
    tasks = []

    for root, _, files in os.walk(input_directory):
        for file in files:
            if not file.endswith('.json'):
                full_path = os.path.join(root, file)
                tasks.append(call_api(full_path, input_directory, output_directory))

    await asyncio.gather(*tasks)









if __name__ == "__main__":


    # Setup - defining folders path for in and out

    '''
    folder_in_path = os.path.join(current_file_directory, "folder_in/images_and_tables/") ## folder with multiple pdfs
    folder_out_path = os.path.join(current_file_directory, "folder_out/images_and_tables/") ## output folder for jsons
    jsonFilePath = os.path.join(folder_out_path,"embedded-images-tables.pdf.json")
    '''
    
    folder_in_path = os.path.join(current_file_directory, "folder_in/attention/") ## folder with multiple pdfs
    folder_out_path = os.path.join(current_file_directory, "folder_out/attention/") ## output folder for jsons
    jsonFilePath = os.path.join(folder_out_path,"attention.pdf.json")
    
    
    # Step 1 - Doing the chunking/extraction - just do it once, to get the json
    asyncio.run(process_files(input_directory=folder_in_path, output_directory=folder_out_path))
    

    # Step 2 - With my function analyteElements
    
    #analysis = analyzeElements(input_json_file_path=jsonFilePath)
    #ic(analysis)



