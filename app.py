import streamlit as st
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

st.set_page_config(page_title="Text Splitter Playground", layout="wide")
st.title("Text Splitter Visualization")
st.write("Experiment with different text splitting strategies in LangChain.")
splitter_type = st.sidebar.selectbox("Splitter Type", ["RecursiveCharacterTextSplitter", "CharacterTextSplitter", "TokenTextSplitter"])
chunk_size = st.sidebar.slider("Chunk Size", min_value=100, max_value=5000, value=1000, step=50)
chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=0, max_value=1000, value=200, step=10)

theme = st.sidebar.selectbox("Theme", ["Light", "Dark", "Neon"])

if theme == "Dark":
    colors = ['#8d6e63', '#5d4037', '#795548', '#a1887f', '#d7ccc8']
elif theme == "Neon":
    colors = ['#FFD700', '#ADFF2F', '#00FFFF', '#FF69B4', '#FFA500']
else: # Light
    colors = ['#ffeeda', '#e0f7fa', '#f3e5f5', '#e8f5e9', '#fff3e0']

if splitter_type == "CharacterTextSplitter":
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
elif splitter_type == "TokenTextSplitter":
    splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
else:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
text_input = st.text_area("Enter Text to Chunk", height=400, placeholder="Paste your text here...")

if st.button("Process"):
    if not text_input:
        st.warning("Please enter some text to process.")
    else:
        chunks = splitter.split_text(text_input)
        st.write(f"Number of chunks: {len(chunks)}")
        
        # Stats
        lengths = [len(c) for c in chunks]
        if lengths:
            avg_len = sum(lengths)/len(lengths)
            st.info(f"Max: {max(lengths)} chars | Min: {min(lengths)} chars | Avg: {avg_len:.2f} chars")
        
        for i, chunk in enumerate(chunks):
            color = colors[i % len(colors)]
            st.markdown(f'<div style="background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px;">{chunk}</div>', unsafe_allow_html=True)


st.markdown('---')
st.caption('Text Splitter Playground | Built with Streamlit & LangChain')


st.sidebar.markdown('---')
st.sidebar.caption('Chunk visuals are color-coded to show boundaries.')
