import streamlit as st
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

st.set_page_config(page_title="Text Splitter Playground", layout="wide")
st.title("Text Splitter Visualization")
