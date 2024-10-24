
#https://github.com/alejandro-ao/U2qfZneHGMNTNEw/tree/solution



# from data.employees import generate_employee_data
import json
import os
import sys
from icecream import ic

from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq


import logging
from l8_assistant import Assistant
from l8_prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from l8_gui import AssistantGUI


data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(data_dir)
#ic(sys.path)
from data.employees import generate_employee_data







if __name__ == "__main__":

    # Here is an example of how to use the get_user_data function
    # users = generate_employee_data(1)[0]
    # print("\n\nUser data:")
    # print(json.dumps(users, indent=4))

    load_dotenv()
    logging.basicConfig(level=logging.INFO)





    

    st.set_page_config(page_title="Umbrella Onboarding - AJ", page_icon="", layout="wide")


    #serialized version of results is stored in the cache
    # this cache is copying the results from the function and hashing them using pickle
    @st.cache_data(ttl=3600, show_spinner="Loading Employee data . . . ")
    def get_user_data():
        return generate_employee_data(1)[0]
    

    # we are not returning a serializable object, but are returning a mutable object, which is DB Client
    # this one is not copying anything, just storing it as is
    @st.cache_resource(ttl=3600, show_spinner="Loading vector store . . . ")
    def init_vector_store(pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap = 200)
            splits = text_splitter.split_documents(docs)

            embedding_function = OpenAIEmbeddings()
            persistent_path = "./data/vectorstore" # persist vectors locally

            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embedding_function,
                persist_directory=persistent_path
            )

            return vectorstore
        
        except Exception as e:
            logging.error(f" Error initializing vector store: { str(e)}")
            st.error(f"Failed to initialize vector stroe: {str(e)}")
            return None
        
        # video (22:20) - probably not a good idea to use classes for data service, because when using streamlit you cannot cache the methods of a class

    customer_data = get_user_data()


    parent_dir = os.path.dirname(os.path.abspath(__file__))
    fileName = os.path.join(parent_dir, "data", "umbrella_corp_policies.pdf")
    
    
    
    vector_store = init_vector_store(fileName)
    

    if "customer" not in st.session_state:
        st.session_state.customer = customer_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"ai", "content": WELCOME_MESSAGE}]


    llm = ChatGroq(model="llama-3.1-8b-instant")

    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm= llm,
        message_history=st.session_state.messages,
        employee_information=st.session_state.customer,
        vector_store=vector_store,
    )

    gui = AssistantGUI(assistant=assistant)
    gui.render()


#if __name__=="__main__":




            





