import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os
import html

st.set_page_config(page_title="Text Splitter Playground", layout="wide")

col1, col2 = st.columns([2, 1])

with col1:
    st.title("Text Splitter Visualization")
    st.write("Experiment with different text splitting strategies in LangChain.")

splitter_type = st.sidebar.selectbox("Splitter Type", ["RecursiveCharacterTextSplitter", "CharacterTextSplitter", "TokenTextSplitter"])

with col2:
    if splitter_type == "RecursiveCharacterTextSplitter":
        st.info("""
        **RecursiveCharacterTextSplitter**
        *   Splits by a prioritized list of separators (e.g., `\\n\\n`, `\\n`, ` `, ``).
        *   Attempts to keep paragraphs, then sentences, then words together.
        *   Best for general text to maintain semantic context.
        """)
    elif splitter_type == "CharacterTextSplitter":
        st.info("""
        **CharacterTextSplitter**
        *   Splits based on a single user-defined separator (default: `\\n\\n`).
        *   Simpler and faster but might break sentences or words if not careful.
        *   Good for strictly formatted text.
        """)
    elif splitter_type == "TokenTextSplitter":
        st.info("""
        **TokenTextSplitter**
        *   Splits text based on token count (using `tiktoken`).
        *   Essential for LLM context windows (e.g., GPT-4 has a token limit).
        *   Might split words in the middle (e.g. "cheeseburger" -> "cheese", "burger").
        """)
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

import tiktoken

# ... (rest of imports)

# Initialize session state for chunks
if 'chunks' not in st.session_state:
    st.session_state.chunks = []

if st.button("Process"):
    if not text_input:
        st.warning("Please enter some text to process.")
    else:
        chunks = splitter.split_text(text_input)
        st.session_state.chunks = chunks

# Check if we have chunks in session state (either from just clicking or previous run)
if st.session_state.chunks:
    chunks = st.session_state.chunks
    
    st.write(f"Number of chunks: {len(chunks)}")
    
    # Calculate Tokens
    enc = tiktoken.get_encoding("cl100k_base")
    token_counts = [len(enc.encode(c)) for c in chunks]
    
    # Stats
    lengths = [len(c) for c in chunks]
    if lengths:
        avg_len = sum(lengths)/len(lengths)
        avg_tokens = sum(token_counts)/len(token_counts)
        st.info(f"""
        **Characters:** Max: {max(lengths)} | Min: {min(lengths)} | Avg: {avg_len:.2f}
        
        **Tokens:** Max: {max(token_counts)} | Min: {min(token_counts)} | Avg: {avg_tokens:.2f}
        """)
        
        st.subheader("Chunk Length Distribution")
        st.bar_chart(lengths)
        
    search_term = st.text_input("Search within chunks", placeholder="Type a keyword to highlight...")
    
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
        # IMPORTANT: Escape HTML to avoid invalid characters or XSS-like issues
        
        # Helper to escape and highlight search term
        def process_text_segment(text):
            escaped = html.escape(text)
            if search_term:
                # Case-insensitive highlight? For now, simple case-sensitive replace
                # To be robust, use regex, but simple replace for demo
                # Highlighting style for search matches: Yellow bg
                highlight = f'<span style="background-color: yellow; color: black; font-weight: bold;">{html.escape(search_term)}</span>'
                return escaped.replace(html.escape(search_term), highlight)
            return escaped

        start_len = len(overlap_prev)
        end_len = len(overlap_next)
        
        if start_len + end_len <= len(chunk):
            part1_text = chunk[:start_len]
            part2_text = chunk[start_len : len(chunk)-end_len]
            part3_text = chunk[len(chunk)-end_len:] if end_len > 0 else ""
            
            # HTML template for overlap highlighting (gray/bold/underlined)
            overlap_style = 'background-color: rgba(255, 255, 255, 0.5); font-weight: bold; text-decoration: underline;'
            
            display_text = ""
            if part1_text:
                display_text += f'<span style="{overlap_style}">{process_text_segment(part1_text)}</span>'
            display_text += process_text_segment(part2_text)
            if part3_text:
                display_text += f'<span style="{overlap_style}">{process_text_segment(part3_text)}</span>'
        else:
            # Fallback for complex overlap
            display_text = process_text_segment(chunk)

        st.markdown(f'<div style="background-color: {color}; padding: 10px; margin: 5px; border-radius: 5px;">{display_text}</div>', unsafe_allow_html=True)


st.markdown('---')
st.caption('Text Splitter Playground | Built with Streamlit & LangChain')


st.sidebar.markdown('---')
st.sidebar.caption('Chunk visuals are color-coded to show boundaries.')
