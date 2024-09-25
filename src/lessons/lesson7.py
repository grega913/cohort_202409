# streamlit crash course
# https://app.alejandro-ao.com/topics/streaming-chat-in-streamlit/

# chat components

import streamlit as st
import time
import requests

st. set_page_config(layout="wide")

# data flow
# https://app.alejandro-ao.com/topics/streamlit-data-flow/
# https://app.alejandro-ao.com/topics/streamlit-session-state/
# https://app.alejandro-ao.com/topics/streamlit-callback-functions/

#region Chat

def chat():

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("ai").markdown(message["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input and user_input != "":

        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        bot_response = f"Echo: {user_input}"
        st.chat_message("ai").markdown(bot_response)
        st.session_state.messages.append({"role": "bot", "content": bot_response})

# using st.write_stream
# https://app.alejandro-ao.com/topics/streaming-chat-in-streamlit/
def chat_with_generator():

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    def generate_response(user_input):
        response = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vehicula tellus quis sapien consequat tempus. Quisque egestas ullamcorper mauris, vel suscipit velit mollis nec. Donec lacinia augue at ex mollis, at congue libero blandit. In in blandit quam, sit amet iaculis dui. Vestibulum dignissim nulla arcu, et pellentesque arcu vulputate in. Morbi dignissim felis rutrum nunc porta consequat. Vivamus vitae odio ligula. Duis molestie libero at lobortis tempor. Quisque feugiat lorem non nunc cursus, eget egestas sapien facilisis. Etiam efficitur malesuada urna quis posuere. Duis iaculis vel enim vel luctus.
        In hac habitasse platea dictumst. Pellentesque vitae erat vulputate, ornare ligula nec, suscipit elit. Ut vitae nibh at lorem mattis cursus vel quis leo. Morbi mi erat, faucibus vitae sapien eget, pulvinar tempus justo. Aliquam vulputate erat a libero iaculis fringilla. Donec posuere diam lobortis cursus vestibulum. Nullam venenatis est lacus, vitae dictum est faucibus non. Proin ut nunc eget mauris elementum porta. Nulla lobortis enim eget justo vestibulum sagittis. Phasellus vel urna arcu. Duis consequat tincidunt lobortis.
        """

        for token in response.split(" "):
            time.sleep(0.01)
            yield token + " "

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("ai").markdown(message["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input and user_input != "":

        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("ai"):
            response_generator = generate_response(user_input)
            response = st.write_stream(response_generator)

        st.session_state.messages.append({"role": "ai", "content": response})


def session_state_details():
    for key in st.session_state.keys():
        st.write(f"{key},: {st.session_state[key]}")


# when we have input widget, we should set up a key param
# this param is than added to the store, and we can access it from any function
def chat_with_callback():

    st.title("Chat with State")
    st.page_link("https://app.alejandro-ao.com/topics/streamlit-callback-functions/", label="AJ_Cohort", icon="🌎")
   
   

    col1, col2, col3 = st.columns([5,2,5])


    with col1:
         # Initialize session state for chat history and input
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Function that is called after every input
        def handle_user_input():
            user_input = st.session_state.user_input
            if user_input:
                # Append user message to session state
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Simple bot response logic
                response = user_input[::-1] # Reverse the user input for fun
                st.session_state.messages.append({"role": "bot", "content": response})


        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("bot"):
                    st.write(message["content"])

        # Input widget for user to send messages
        st.chat_input("Your message", key="user_input", on_submit=handle_user_input)




        
    with col2:
        #display session state
        session_state_details()

    with col3:
        code = '''         # Initialize session state for chat history and input
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Function that is called after every input
        def handle_user_input():
            user_input = st.session_state.user_input
            if user_input:
                # Append user message to session state
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Simple bot response logic
                response = user_input[::-1] # Reverse the user input for fun
                st.session_state.messages.append({"role": "bot", "content": response})


        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("bot"):
                    st.write(message["content"])

        # Input widget for user to send messages
        st.chat_input("Your message", key="user_input", on_submit=handle_user_input)'''

        st.code(code, language="python")

def chat_with_arguments():

    def handle_user_input(user_input, bot_name="Bot", emotion="neutral"):
        if user_input:
            st.write(f"I am {bot_name} and I am ({emotion}). You said: {user_input}")

    user_input = st.text_input("Write something")

    # Button that triggers the callback function
    st.button(
        "Send Message", 
        on_click=handle_user_input, 
        args=(user_input,),  # Passing the user input as a positional argument
        kwargs={"bot_name": "AI Assistant", "emotion": "happy"}  # Passing bot_name and emotion as keyword arguments
    )

#endregion

#region Cache
#https://app.alejandro-ao.com/topics/streamlit-cache/
def test_cache_data():

    st.title("Caching")

    st.markdown("Should know difference between cach_data and cache_resource")


    #@st.cache_data
    def fetch_data(api_url):
        response = requests.get(api_url)
        time.sleep(3)
        return response.json()
    
    data = fetch_data("https://dog.ceo/api/breeds/image/random")
    st.write(data)

    st.image(data["message"], caption="Random dog image")
    st.button("Reload page")



def test_cache_resource():
    class AiModel:
        def __init__(self):
            # Load model
            time.sleep(5)
            self.model = "model"

        def predict(self, input_data):
            return "prediction"

    @st.cache_resource(show_spinner="Loading Model...", ttl=3600)
    def load_model():
        model = AiModel()
        return model

    model = load_model()
    if model:
        st.write("Model Loaded")

    st.button("reload page")
    


#endregion







if __name__=="__main__":
    #chat()
    # chat_with_generator()
    # chat_with_callback()
    # chat_with_arguments()
    # test_cache_data()
    test_cache_resource()