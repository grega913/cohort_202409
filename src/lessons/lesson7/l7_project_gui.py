
import streamlit as st
import time
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import time

# region Lesson7Topic10 - Graphical UI for AIAssistant

# lesson7, topic 10 - https://app.alejandro-ao.com/topics/project-your-gui-ai-assistant/
# using st.write_stream
# https://app.alejandro-ao.com/topics/streaming-chat-in-streamlit/
# connect with our chat with history from lesson5

def st_chat_with_generator():
    printWithTime("def st_chat_with_generator")

    # first we initialize chain we're gonna be invoking 
    chain_with_message_history = get_chain_with_message_history()

    # we define messages in st.session_state so that we can display the mwith streamlit    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # internal function for building a generator we'll use in write_stream
    # we use this, when we are using .invoke on Runnable
    # if we use .stream, we don't need this function
    def generate_response(str: str):
        for token in str.split(" "):
            time.sleep(0.04)
            yield token + " "


    # main part displaying messages from the state
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("ai").markdown(message["content"])

    user_input = st.chat_input("Type your message here...")


    if user_input and user_input != "":

        # first we append message to messages
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # we invoke the chain to get the response
        '''
        chain_response = chain_with_message_history.invoke(
            {"input": user_input},
            {"configurable": {"session_id": "abc123"}},
        )
        '''
        # we use stream method to stram the generation so we can put it straing into write_stream
        chain_response_stream = chain_with_message_history.stream(
            {"input": user_input},
            {"configurable": {"session_id": "abc123"}},
        )


        # testing what is in session_history
        # if we don't cache the def get_chain_with_message_history, this is always empty, and conversation has no memory/chat _history, because the function gets called every time
        # we run streamlit
        history = chain_with_message_history.get_session_history("abc123")

        printWithTime("history: " + str(history))
        printWithTime("------------------------")


        # displaying response from the chain within st.chat_mesage("ai")
        with st.chat_message("ai"):
            '''
            response_generator = generate_response(chain_response.content)
            response = st.write_stream(response_generator)
            '''
            response=st.write_stream(chain_response_stream)
                
        # adding message to the messages in state
        st.session_state.messages.append({"role": "ai", "content": response})



# function that returns chain. We'll be invoking this in other function.
# by setting st.cache_resource, this only runs single time when called in other function. If this is not cached, ChetMessageHistory would not work, as it would initialize every time streamlit refreshes
@st.cache_resource()
def get_chain_with_message_history():

    printWithTime("get_chain_with_message_history")

    model = ChatGroq()
    chat_history = ChatMessageHistory()
    # session_id=[]  not needed here 

    prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system", "You are a helpful assistant. Answer all questions to the best of your ability. The provided chat history includes facts about the user you are speaking with.",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    chain = prompt | model

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return chain_with_message_history




# endregion






# version where chat_history serves as input to another chain to make context of messages
def st_chat_history_final(user_message):

    model = ChatGroq()
    chat_history = ChatMessageHistory()

    session_id = []

    chat_history.add_user_message(user_message)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system", "You are a helpful assistant. Answer all questions to the best of your ability. The provided chat history includes facts about the user you are speaking with.",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    chain = prompt | model

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )


    




    response = chain_with_message_history.invoke(
        {"input": user_message},
        {"configurable": {"session_id": "unused"}},
    )

    print("Response:", response)


    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            (
                "user","Distill the above chat messages into a single summary message. Include as many specific details as you can.",
            ),
        ]
    )

    summarization_chain = summarization_prompt | model

    summary_message = summarization_chain.invoke({"chat_history": chat_history.messages})

    chat_history.clear()

    chat_history.add_message(summary_message)



    return response



    print("Summary:", summary_message)


def printWithTime(str):
    current_time = time.strftime("%H:%M:%S", time.gmtime(time.time()))
    print(current_time + " " + str)



if __name__ == "__main__":
    print("lesson7_project_gui.py")