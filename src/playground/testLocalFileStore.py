from langchain.storage import LocalFileStore
import os
from icecream import ic






# Instantiate the LocalFileStore with the root path
# file_store = LocalFileStore(data_dir)




if __name__=="__main__":
    data_dir = os.path.dirname(os.path.abspath(__file__))
    fileStorePath = os.path.join(data_dir, "myFileStore")
    file_store = LocalFileStore(fileStorePath)

    # Set values for keys
    file_store.mset([
        ("key1", b"GyYhKQxW"),
        ("key2", b"F7d3a9b2"),
        ("key3", b"E1c2a3b4"),
        ("key4", b"R5t6y7u8"),
        ("key5", b"N3m2l1k"),
        ("key6", b"P9o8n7m"),
        ("key7", b"I4h3g2f"),
        ("key8", b"S6d5c4b"),
        ("key9", b"T8r7q6p"),
        ("key10", b"A2z1y9x")
        ])

    # Get values for keys
    values = file_store.mget(["key1", "key2"])  # Returns [b"value1", b"value2"]
    ic(values)

    # Delete keys
    file_store.mdelete(["key1"])

    # Iterate over keys
    for key in file_store.yield_keys():
        ic(key)
        ic(file_store.mget([key]))

   
    
