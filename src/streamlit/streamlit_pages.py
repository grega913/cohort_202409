import streamlit as st

# Create a Streamlit app
st.set_page_config(page_title="My App", page_icon=":smile:", layout="wide")

# Initialize the state
if 'my_variable' not in st.session_state:
    st.session_state.my_variable = None

# Create a navigation menu
pages = {
    "Info": "info",
    "About": "about",
    "Contact": "contact"
}

selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))

# Create the pages
if selected_page == "Info":
    st.title("Info Page")
    st.write("This is the info page.")
    st.write("You can add more content here.")
    st.write("Enter a value:")
    my_input = st.text_input("Input", value=st.session_state.my_variable)

    # Create a button to save the input
    if st.button("Save"):
        st.session_state.my_variable = my_input


elif selected_page == "About":
    st.title("About Page")
    st.write("This is the about page.")
    st.write("You can add more content here.")
    st.write("The value is:", st.session_state.my_variable)
elif selected_page == "Contact":
    st.title("Contact Page")
    st.write("This is the contact page.")
    st.write("You can add more content here.")