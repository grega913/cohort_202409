# example from https://docs.unstructured.io/examplecode/codesamples/oss/vector-database

from unstructured.partition.html import partition_html
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOpenAI

from icecream import ic

# Gather Links with Unstructured
cnn_lite_url = "https://lite.cnn.com/"
elements = partition_html(url=cnn_lite_url)
links = []

for element in elements:
    if element.metadata.link_urls:
        relative_link = element.metadata.link_urls[0][1:]
        if relative_link.startswith("2024"):
            links.append(f"{cnn_lite_url}{relative_link}")


# Ingest Individual Articles with UnstructuredURLLoader
loaders = UnstructuredURLLoader(urls=links, show_progress_bar=True)
docs = loaders.load()

# Load Documents into ChromaDB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)


# Summarize the documents
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
chain = load_summarize_chain(llm, chain_type="stuff")


if __name__=="__main__":

    query_docs = vectorstore.similarity_search("Who will host SNL.", k=1)
    response = chain.invoke(query_docs)
    ic(response)
