
# this is local version of the colab code for Alejandro's Cohort
# Lesson 5
# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw?pli=1&usp=drive_fs#scrollTo=XR-acFrZjkZF


import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()  # Load the .env file

# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=XR-acFrZjkZF
# Define our function

# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=GJA4MC5kpWia
def lesson5topic4():

    def get_weather_of(city):
        if city == "Paris":
            return "cloudy"
        if city == "London":
            return "rainy"
        return "sunny"

# Define a prompt template - single variable
    template = "What should I wear if the weather today is {weather}?"
    prompt = ChatPromptTemplate.from_template(template)

    # Model (can be any supported LLM)
    model = ChatGroq()

    # Output parser
    output_parser = StrOutputParser()

    # Chain with function coercion
    weather_chain = (
        #Example 1: Coercing a Function with a Lambda Expression
        #(lambda input: get_weather_of(input)) |

        #Example 2: Coercing a Function with JSON Syntax
        {"weather": lambda input: get_weather_of(input)} |      # Coerced function
        prompt |                                                # Prompt template
        model |                                                 # LLM model
        output_parser                                           # Output parser
    )

    # Try it out
    result = weather_chain.invoke("NY")
    print(result)

    return result # need return when using streamlit


# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=4Ck574FS6_bD
def lesson5topic5():
    # Define two functions
    def get_temperature(city):
        if city == "Paris":
            return 15
        if city == "London":
            return 10
        if city == "San Francisco":
            return 20
        return 25

    def get_weather(city):
        if city == "Paris":
            return "cloudy"
        if city == "London":
            return "rainy"
        return "cloudy"

    # Define the prompt
    prompt = ChatPromptTemplate.from_template(
        "What should I wear if the weather is {weather} and the temperature is {temperature} degrees Celsius?"
    )

    print(prompt)

    # Create the chain
    chain = (prompt | ChatGroq() | StrOutputParser())

    # Use RunnableParallel to run functions concurrently
    composed_chain = (
        {
            "weather": lambda input: get_weather(input),
            "temperature": lambda input: get_temperature(input)
        }
        | chain
    )

    # Invoke the chain
    result = composed_chain.invoke("San Francisco")
    print(result)

# Running multiple Chains in Parallel
# https://colab.research.google.com/drive/1KqAecRG0bPAsv-0ouGYtbJMMKnq2-3Uw#scrollTo=RXrHwpI47GJw
def lesson5topic5_2(topic = "Rambo"):
    # Define the model and parser
    model = ChatGroq()
    output_parser = StrOutputParser()

    # First Chain: Poem Generation

    # Define the prompt
    prompt_template = "Write a poem about {topic}"
    prompt = ChatPromptTemplate.from_template(prompt_template)


    # Create the poem chain
    poem_chain = prompt | model | output_parser

    # Test the chain
    result_1 = poem_chain.invoke(topic)
    print(result_1)

    # Second Chain: Story Generation

    # Define the prompt
    prompt_template_2 = "Write a 3 sentence story about {topic}"
    prompt_2 = ChatPromptTemplate.from_template(prompt_template_2)

    # Create the poetic story chain
    story_chain = prompt_2 | model | output_parser

    # Test the chain
    result_2 = story_chain.invoke(topic)
    print(result_2)



    # Composed Chain: Comparing Poem and Prose
    # Define the comparison prompt
    comparison_template = """
    Which of these literary pieces is of better quality?
    A poem:
    {poem}

    A story in prose:
    {story}
    """
    comparison_prompt = ChatPromptTemplate.from_template(comparison_template)

    # Create the comparison chain
    comparison_chain = comparison_prompt | model | output_parser

    # Use RunnableParallel to run both chains concurrently
    composed_chain = (
        {
            "poem": poem_chain,
            "story": story_chain
        }
        | comparison_chain
    )

    # Invoke the composed chain
    result = composed_chain.invoke({"topic": topic})
    print(result)

'''
# Alternative Methods Using RunnableParallel Class
from langchain_core.runnables import RunnableParallel

# Use RunnableParallel class for the same result

composed_chain = {
    "poem": poem_chain,
    "story": story_chain
} | comparison_prompt | model | output_parser

# Or use the class constructor
composed_chain = RunnableParallel({
    "poem": poem_chain,
    "story": story_chain
}) | comparison_prompt | model | output_parser

# Or use named arguments
composed_chain = RunnableParallel(poem=poem_chain, story=story_chain) | comparison_prompt | model | output_parser

# Invoke the composed chain
result = composed_chain.invoke({"topic": topic})
print(result)
'''










if __name__ == "__main__":
    # Your main code goes here
    lesson5topic5_2()