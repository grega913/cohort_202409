# code for Project: Wikipedia to Blog Post from https://app.alejandro-ao.com/topics/project-wikipedia-to-blog-post/
# this is colab's version: https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=Z20dWLJ32uw7


from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import WikipediaRetriever
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()  # Load the .env file

# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=Z20dWLJ32uw7
def wikiToBlog(article = "John Wayne"):
    # using LangChain's WikipediaRetriever to retrieve data from Wikipedia
    retriever = WikipediaRetriever()

    # invoke method on retriver returns list of documents
    docs = retriever.invoke(article)

    # we are only using the page_content of first document as a doc_content - KISS
    doc_content = docs[0].page_content

    article_prompt = ChatPromptTemplate.from_template(
        """
        Following is an wikipedia article about {article}. Please identify from 3 to 5 main concepts described in the article.
        For each of the concepts give it a self-described name, and provide a short summary, max 2 sentences, of it. This is the article: {doc_content}.
        Result should be in the JSON format, where the keys will be before mentioned self-described names, and value will be short summaries.
        """
    )

    # Model (can be any supported LLM)
    model = ChatGroq()

    # Output parser
    # output_parser = StrOutputParser()

    # defining the class that is needed for JSON Parser
    # https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/json/
    class BlogConcept(BaseModel):
        concept: str = Field(description="Name of the concept")
        summary: str = Field(description="Summary of the concept")

    article_output_parser = JsonOutputParser(pydantic_object=BlogConcept)


    # creating and invoking a chain
    article_chain = article_prompt | model | article_output_parser
    article_result = article_chain.invoke({"article": article, "doc_content": doc_content})
    print(article_result)
    print(type(article_result))

    # loop through the article_result dictionary
    def loop_through_dict(input_param):
        if not isinstance(input_param, dict):
            print("Error: Input parameter is not a dictionary")
            return

        for key, value in input_param.items():
            print(f"Key: {key}, Value: {value}")

    # loop_through_dict(article_result)

    blog_prompt = ChatPromptTemplate.from_template(
        """
        You are an experienced blog writer about various topics. Please write a blog post in informative and humorous way. Blog should be written based on the provided dictionary.
        Loop through the the provided dictionary. Each paragraph in a blog post should have a title, which is a key from input {article_result}. If the key is not provided, you should create one based on the paragraph content. There should be about 10 sentences in each paragraph.
        This is the dictionary: {article_result}.
        """
    )

    blog_output_parser = StrOutputParser()

    blog_chain = blog_prompt | model | blog_output_parser
    blog_result = blog_chain.invoke({"article_result": article_result})
    print(blog_result)

    return blog_result


if __name__ == "__main__":
    # Your main code goes here
    wikiToBlog()
