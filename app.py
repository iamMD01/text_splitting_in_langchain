import streamlit as st
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter

st.set_page_config(page_title="Text Splitter Playground", layout="wide")
st.title("Text Splitter Visualization")
st.write("Experiment with different text splitting strategies in LangChain.")
splitter_type = st.sidebar.selectbox("Splitter Type", ["RecursiveCharacterTextSplitter", "CharacterTextSplitter"])
chunk_size = st.sidebar.slider("Chunk Size", min_value=100, max_value=5000, value=1000, step=50)
chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=0, max_value=1000, value=200, step=10)

if splitter_type == "CharacterTextSplitter":
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
else:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
text_input = st.text_area("Enter Text to Chunk", height=400, placeholder="Paste your text here...")

if st.button('Process'):
    st.write('Processing...')
