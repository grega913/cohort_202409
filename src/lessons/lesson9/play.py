import sqlite3
import os
from icecream import ic
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.storage import SQLStore
import time
from database import COLLECTION_NAME
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def createSqliteDbInSameFolder(name="sq_test.db"):
    ic(f"def createSqliteDbInSameFolder with name {name} ")
    current_file_directory = os.path.dirname(__file__)
    sqlitepath = os.path.join(current_file_directory, name)
        
    conn = sqlite3.connect(sqlitepath)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE langchain_key_value_stores (
            key TEXT PRIMARY KEY,
            value BLOB,
            namespace TEXT
        );
        '''
    )

    conn.commit()
    conn.close()

    ic("done creating sqlite db")

def insertDummyRecordsIntoDb(name="sq_test.db"):
    ic(f"def insertDummyRecordsIntoDb with name {name} ")
    current_file_directory = os.path.dirname(__file__)
    sqlitepath = os.path.join(current_file_directory, name)
    
    conn = sqlite3.connect(sqlitepath)
    c = conn.cursor()
    
    dummy_records = [
        ("key11", b"value1", "namespace"),
        ("key12", b"value2", "namespace"),
        ("key13", b"value3", "namespace"),
        ("key14", b"value4", "namespace"),
        ("key15", b"value5", "namespace"),
    ]
    
    for key, value, namespace in dummy_records:
        c.execute("INSERT INTO langchain_key_value_stores VALUES (?, ?, ?)", (key, value, namespace))
    
    conn.commit()
    conn.close()

    ic("done inserting dummy records into db")

def queryAllRecordsFromDb(name="sq_test.db"):
    ic(f"def queryAllRecordsFromDb with name {name} ")
    current_file_directory = os.path.dirname(__file__)
    sqlitepath = os.path.join(current_file_directory, name)
    
    conn = sqlite3.connect(sqlitepath)
    c = conn.cursor()
    
    c.execute("SELECT * FROM langchain_key_value_stores")
    
    records = c.fetchall()
    
    for record in records:
        ic(f"Key: {record[0]}, Value: {record[1]}, Namespace: {record[2]}")
    
    conn.close()

    ic("done querying all records from db")


def setSQLStore(namespace = "langchain_key_value_stores", name="sq_test.db"):
    ic("def setSQLStore")
    current_file_directory = os.path.dirname(__file__)
    sqlitepath = os.path.join(current_file_directory, name)

    db_url="sqlite:///" + str(sqlitepath)
    ic(db_url)


    sql_store = SQLStore(namespace=namespace, db_url=db_url)


    #all_keys = list(sql_store.yield_keys())
    #ic(all_keys)

    #values = sql_store.mget(all_keys)
    #ic(values)

    # sql_store.mset([("key22", b"value18"), ("key23", b"value19")])
    
    

    # Get all keys and values in a single step
    all_key_value_pairs = {key: sql_store.mget([key])[0] for key in sql_store.yield_keys()}

    # Print or use the key-value pairs
    for key, value in all_key_value_pairs.items():
        ic(f"Key: {key}, Value: {value}") 


    

    # Delete all keys and their associated values
    # all_keys = list(sql_store.yield_keys())
    # sql_store.mdelete(all_keys)     
    # ic("after deletion")



    ic("end def setSQLStore")




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


if __name__=="__main__":


    #createSqliteDbInSameFolder()
    #insertDummyRecordsIntoDb()
    #queryAllRecordsFromDb()

    # setSQLStore()

    retriever = simpleMultiVectorRetriever()
    ic(retriever)



    '''
    
    sql_store = SQLStore(namespace="langchain_key_value_stores", db_url="sqlite:///test.db")

    # Set values for keys
    #sql_store.mset([("key1", b"value1"), ("key2", b"value2")])

    # Get values for keys
    #values = sql_store.mget(["key1", "key2"])  # Returns [b"value1", b"value2"]

    # Delete keys
    # sql_store.mdelete(["key1"])

    # Iterate over keys
    #for key in sql_store.yield_keys():
     #   print(key)
    
    values = sql_store.mget(list(sql_store.yield_keys()))
    ic(values)
    '''
