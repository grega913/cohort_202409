#https://docs.trychroma.com/getting-started

import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is something else",
        "bla bla"
    ],
    ids=["id1", "id2", "id3", "id5"]
)


results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)

