# Basics

# Process an individual file by using the Unstructured Python SDK
# https://docs.unstructured.io/api-reference/api-services/sdk-python

import os, json

import unstructured_client
from unstructured_client.models import shared
from icecream import ic
import time
from dotenv import load_dotenv
load_dotenv()  # Load the .env file

current_file_name = os.path.basename(__file__)
dir_name = os.path.dirname(os.path.basename(__file__))
current_file_directory = os.path.dirname(__file__)
ic(current_file_name)
ic(current_file_directory)


client = unstructured_client.UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
    server_url=os.getenv("UNSTRUCTURED_API_URL"),
)

fileNameInPath = os.path.join(current_file_directory, "folder_in\\attention\\attention.pdf")
filename = fileNameInPath

fileNameOutPath = os.path.join(current_file_directory, "folder_out\\attention\\attention.json")




req = {
    "partition_parameters": {
        "files": {
            "content": open(filename, "rb"),
            "file_name": filename,
        },
        "strategy": shared.Strategy.HI_RES,
        "languages": ['eng'],
        "split_pdf_page": True,            # If True, splits the PDF file into smaller chunks of pages.
        "split_pdf_allow_failed": True,    # If True, the partitioning continues even if some pages fail.
        "split_pdf_concurrency_level": 15  # Set the number of concurrent request to the maximum value: 15.
    }
}

try:
    res = client.general.partition(request=req)
    element_dicts = [element for element in res.elements]

    # Print the processed data's first element only.
    print(element_dicts[0])

    # Write the processed data to a local file.
    json_elements = json.dumps(element_dicts, indent=2)

    with open(fileNameOutPath, "w") as file:
        file.write(json_elements)
except Exception as e:
    print(e)


