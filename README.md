# Text Splitter & Chunking Visualizer ✂️

A powerful, interactive Streamlit application designed to help developers and researchers understand, visualize, and debug **Text Splitting** strategies for Large Language Models (LLMs) and RAG (Retrieval-Augmented Generation) pipelines.

---

## 🚀 Features

*   **Interactive Playground:** Real-time visualization of how different splitters break down text.
*   **Multiple Splitter Types:**
    *   `RecursiveCharacterTextSplitter`: The industry standard for semantic splitting.
    *   `CharacterTextSplitter`: Simple, separator-based splitting.
    *   `TokenTextSplitter`: Splits based on token counts (using `tiktoken`), crucial for LLM context windows.
*   **Deep Visualization:**
    *   **Color-Coded Chunks:** Easily distinguish between adjacent text segments.
    *   **Overlap Highlighting:** See exactly where chunks overlap to ensure context preservation.
    *   **Dynamic Graphs:** Bar charts showing the distribution of chunk lengths.
    *   **Token Counters:** Real-time token usage stats (Max/Min/Avg).
*   **Search & Highlight:** Instantly find keywords across all chunks with highlighter support.
*   **PDF Support:** Upload and process PDF documents directly.
*   **State Management:** Search and interact without losing your processed data.

---

## 📚 Documentation (For Presentation & Synopsis)

We have included detailed documentation within this repository to help with your project reports and presentations:

1.  **[Text Splitting Concepts (Concepts & Theory)](text_splitting_concepts.md)**
    *   Explains *why* we chunk text, context windows, and RAG.
    *   Compares different algorithms.
    *   Great for the "Introduction" and "Methodology" sections of your report.

2.  **[Project Implementation (Code & Architecture)](project_implementation.md)**
    *   Technical deep-dive into the code structure (`app.py`).
    *   Explains session state, HTML escaping, and Streamlit components.
    *   Great for the "Technical Implementation" section.

---

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/iamMD01/text_splitting_in_langchain.git
    cd text_splitting_in_langchain
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Usage

1.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  Open your browser at `http://localhost:8501`.

3.  **Experiment:**
    *   Paste text or upload a PDF.
    *   Select a splitter type from the sidebar.
    *   Adjust `Chunk Size` and `Chunk Overlap`.
    *   Click **Process** and explore the results!

---

## 🧩 Tech Stack

*   **Frontend:** Streamlit
*   **Logic:** LangChain (Text Splitters)
*   **Tokenization:** Tiktoken (OpenAI)
*   **Data Processing:** PyPDF

