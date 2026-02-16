import streamlit as st
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

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

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

if uploaded_file:
    # Use a fixed suffix so PyPDFLoader knows it's a PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    
    try:
        loader = PyPDFLoader(tmp_file_path)
        docs = loader.load()
        text_input = "\n".join([doc.page_content for doc in docs])
        st.success("PDF loaded successfully! Content extracted.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        text_input = "" # Fallback or keep previous? Better to clear or show empty.
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
else:
    text_input = st.text_area("Enter Text to Chunk", height=400, placeholder="Paste your text here...", value="LangChain is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model via an API, but will also: Be data-aware: connect a language model to other sources of data. Be agentic: allow a language model to interact with its environment. As such, the LangChain framework is designed with the objective in mind to enable those types of applications.")

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
            
            overlap_prev = ""
            overlap_next = ""
            
            # Check overlap with previous chunk (at the start of current chunk)
            if i > 0:
                prev_chunk = chunks[i-1]
                max_check = len(chunk)
                for k in range(max_check, 0, -1):
                    suffix = prev_chunk[-k:]
                    prefix = chunk[:k]
                    if suffix == prefix:
                        overlap_prev = prefix
                        break
            
            # Check overlap with next chunk (at the end of current chunk)
            if i < len(chunks) - 1:
                next_chunk = chunks[i+1]
                max_check = len(chunk)
                for k in range(max_check, 0, -1):
                    suffix = chunk[-k:]
                    prefix = next_chunk[:k]
                    if suffix == prefix:
                        overlap_next = suffix
                        break
            
            # Construct display HTML
            display_text = chunk
            
            # We need to handle cases where overlap_prev and overlap_next might overlap each other (small chunks)
            # But for simple visualization, let's assume standard chunking where overlap < chunk_size/2
            
            if overlap_next:
                 # Highlight end
                 non_overlap_len = len(chunk) - len(overlap_next)
                 display_text = chunk[:non_overlap_len] + f'<span style="background-color: rgba(255, 255, 255, 0.5); font-weight: bold; text-decoration: underline;">{overlap_next}</span>'
            
            if overlap_prev:
                # Highlight start
                # We need to be careful not to double-replace if we already modified display_text
                # If we modified end, the start is still intact at index 0
                soup = display_text # simplistic
                
                # Re-construct:
                # Part 1: Overlap Prev
                # Part 2: Middle (Non-overlap)
                # Part 3: Overlap Next
                
                start_len = len(overlap_prev)
                end_len = len(overlap_next)
                
                if start_len + end_len > len(chunk):
                     # Overlaps intersect - fringe case, just highlight everything or handle gracefully
                     # For now, let's just highlight start and whatever is left of end?
                     # Simpler: just highlight start, middle, end based on indices
                     pass 
                
                part1 = f'<span style="background-color: rgba(255, 255, 255, 0.5); font-weight: bold; text-decoration: underline;">{chunk[:start_len]}</span>'
                part3 = f'<span style="background-color: rgba(255, 255, 255, 0.5); font-weight: bold; text-decoration: underline;">{chunk[-end_len:]}</span>' if end_len > 0 else ""
                
                if start_len + end_len <= len(chunk):
                    part2 = chunk[start_len : len(chunk)-end_len]
                    display_text = part1 + part2 + part3
                else:
                    # Overlap region implies the whole chunk is basically overlap
                    display_text = part1 + chunk[start_len:] # simplified fallback

            st.markdown(f'<div style="background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px;">{display_text}</div>', unsafe_allow_html=True)


st.markdown('---')
st.caption('Text Splitter Playground | Built with Streamlit & LangChain')


st.sidebar.markdown('---')
st.sidebar.caption('Chunk visuals are color-coded to show boundaries.')
