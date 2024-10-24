# code for project ConversationalChain from https://app.alejandro-ao.com/topics/project-conversational-chain/
# this is colab's version: https://colab.research.google.com/drive/1Byudj38Hfaph9et0zGb1Jb8sV1K9F2ad?pli=1&usp=drive_fs#scrollTo=mV8Npw8f1kqq

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from icecream import ic


from dotenv import load_dotenv
load_dotenv()  # Load the .env file

model = ChatGroq()





def message_passing():
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        ("placeholder", "{messages}"),
    ]
    )   

    chain = prompt | model

    ai_msg = chain.invoke(
        {
            "messages": [
                (
                    "human",
                    "Translate this sentence from English to French: I love programming.",
                ),
                ("ai", "J'adore la programmation."),
                ("human", "What did you just say?"),
            ],
        }
    )
    print(ai_msg.content)

def chat_history():
    ic("chat_history")

    demo_ephemeral_chat_history = ChatMessageHistory()

    demo_ephemeral_chat_history.add_user_message(
        "Translate this sentence from English to French: I love programming."
    )

    demo_ephemeral_chat_history.add_ai_message("J'adore la programmation.")

    ic(demo_ephemeral_chat_history.messages)

def chat_history_2():
    demo_ephemeral_chat_history = ChatMessageHistory()


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer all questions to the best of your ability.",
            ),
            ("placeholder", "{messages}"),
        ]
    )   

    chain = prompt | model




    input1 = "Translate this sentence from English to French: I love programming."

    demo_ephemeral_chat_history.add_user_message(input1)


    

    response = chain.invoke(
        {
            "messages": demo_ephemeral_chat_history.messages,
        }
    )

    demo_ephemeral_chat_history.add_ai_message(response)

    input2 = "What did I just ask you?"

    demo_ephemeral_chat_history.add_user_message(input2)

    result = chain.invoke(
        {
            "messages": demo_ephemeral_chat_history.messages,
        }
    )
    # ic(result)
    return result

def chat_history_final():
    demo_ephemeral_chat_history = ChatMessageHistory()

    session_id = []

    while True:
        user_message = input("You: ")
        print("user_message: ", user_message)
        if user_message.lower() in ["stop", "over", "end", "ciao"]:
            print("Stopping!!!")
            break

        demo_ephemeral_chat_history.add_user_message(user_message)

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
            lambda session_id: demo_ephemeral_chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        response = chain_with_message_history.invoke(
            {"input": user_message},
            {"configurable": {"session_id": "unused"}},
        )

        print("Assistant:", response)

        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                ("placeholder", "{chat_history}"),
                (
                    "user","Distill the above chat messages into a single summary message. Include as many specific details as you can.",
                ),
            ]
        )


        summarization_chain = summarization_prompt | model

        summary_message = summarization_chain.invoke({"chat_history": demo_ephemeral_chat_history.messages})

        demo_ephemeral_chat_history.clear()

        demo_ephemeral_chat_history.add_message(summary_message)

        print("Summary:", summary_message)




    
    demo_ephemeral_chat_history = ChatMessageHistory()

    session_id = []

    demo_ephemeral_chat_history.add_user_message(user_message)

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
        lambda session_id: demo_ephemeral_chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    response = chain_with_message_history.invoke(
        {"input": user_message},
    {"configurable": {"session_id": "unused"}},
    )

    print("Assistant:", response)

    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            (
                "user","Distill the above chat messages into a single summary message. Include as many specific details as you can.",
            ),
        ]
    )


    summarization_chain = summarization_prompt | model

    summary_message = summarization_chain.invoke({"chat_history": demo_ephemeral_chat_history.messages})

    demo_ephemeral_chat_history.clear()

    demo_ephemeral_chat_history.add_message(summary_message)

    print("Summary:", summary_message)






if __name__ == "__main__":
    print("let's go")
    # message_passing()
    # chat_history()
    # res = chat_history_2()
    # ic(res)
    chat_history_final()
    
