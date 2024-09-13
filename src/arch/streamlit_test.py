import streamlit as st
import pandas as pd
import numpy as np


from lesson5 import lesson5topic4

st.title('COHORT')

st.text_area("Text to translate")
st.date_input("Your birthday")
st.time_input("Meeting time")
st.file_uploader("Upload a CSV")
st.camera_input("Take a picture")
st.color_picker("Pick a color")

st.write("Most objects") # df, err, func, keras!
st.write(["st", "is <", 3]) # see *


st.text("Fixed width text")
st.markdown("_Markdown_") # see *
st.latex(r""" e^{i\pi} + 1 = 0 """)
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")
st.html("<p>Hi!</p>")

