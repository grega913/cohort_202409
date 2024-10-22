import os
import sys

import streamlit as st
import streamlit.components as stc

import pandas as pd
import numpy as np
import importlib.util



# Get the parent directory's path
parent_dir = os.path.dirname(os.path.dirname(__file__))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from lessons.l5 import lesson5topic4, lesson5topic5, lesson5topic5_2
from lessons.l5_project_wiki import wikiToBlog




st.title('COHORT')



st.markdown("---")


input_article = st.text_input("Enter article from which a blog post will be generated.:")
if st.button("create blog post"):
    result_article = wikiToBlog(article=input_article)
    st.text_area("Answer from the function", value=str(result_article))

st.markdown("---")
st.markdown("---")
st.markdown("---")
st.markdown("---")
st.markdown("---")


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

