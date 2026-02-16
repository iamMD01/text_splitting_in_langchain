# Project Implementation: Text Splitter Visualizer

This document details the **technical implementation** and **project structure** of the Text Splitter Visualizer application. It is designed to help improved understanding of *how* the code works for technical presentations and synopsis writing.

---

## 1. Project Overview & Tech Stack

This project is a **Streamlit** web application that allows users to experiment with and visualize how different **LangChain** text splitters process text.

*   **Language:** Python 3.x
*   **Web Framework:** Streamlit (chosen for rapid UI development and interactive widgets).
*   **Core Logic:** LangChain (standard library for building LLM applications, specifically its `text_splitters` module).
*   **Tokenization:** `tiktoken` (OpenAI's BPE tokenizer, used for accurate token counting).
*   **PDF Processing:** `pypdf` (for extracting text from uploaded PDFs).

---

## 2. Directory Structure

The project follows a clean, single-file application structure, which is common for Streamlit demos.

```
text_splitter_and_chunking_in_langchain/
├── .streamlit/
│   └── config.toml      # Configuration file for enforcing the Light Theme globally.
├── .gitignore           # Specifies files to ignore in Git (e.g., .venv, __pycache__).
├── README.md            # General project documentation.
├── app.py               # MAIN APPLICATION FILE (Contains all logic).
├── requirements.txt     # List of Python dependencies (streamlit, langchain, etc.).
└── text_splitting_concepts.md # Conceptual guide (this document's companion).
```

---

## 3. Code Breakdown (`app.py`)

The application logic is centralized in `app.py`. Here is a step-by-step breakdown of its components:

### A. Imports & Configuration
*   **`streamlit`**: Manages the UI.
*   **`langchain_text_splitters`**: Imports the specific splitter classes (`Recursive`, `Character`, `Token`).
*   **`html`**: Critical for escaping special characters to prevent rendering errors (XSS protection).
*   **`tiktoken`**: Used to calculate the exact number of tokens in each chunk.

### B. UI Layout (Columns)
We use `st.columns([2, 1])` to create a 2-column layout:
*   **Left (2/3):** Main Content (Title, Chunks, Search).
*   **Right (1/3):** Dynamic Information (Explains the currently selected splitter).

### C. The Sidebar (Controls)
The sidebar acts as the "Control Panel":
1.  **Splitter Type:** A dropdown to select the algorithm.
2.  **Chunk Size:** Slider (100 - 5000 characters). Controls the maximum size of a chunk.
3.  **Chunk Overlap:** Slider (0 - 1000 characters). Controls the sliding window overlap.
4.  **File Uploader:** Accepts PDF files. Logic handles saving to a temp file, reading with `PyPDFLoader`, and cleaning up.
5.  **Theme Selector:** (Legacy toggle, now largely superseded by `config.toml` but still functional for manual overrides).

### D. State Management (`st.session_state`)
**Crucial for UX:** We use `st.session_state` to **persist** the generated chunks.
*   *Problem:* Without this, typing in the "Search" box would trigger a full app rerun, resetting the `chunks` variable and making the results disappear.
*   *Solution:* We store `chunks` in the session. The "Process" button updates this state. The Search box reads *from* this state, allowing realtime highlighting without re-processing the text.

### E. The Splitting Logic
Based on the user's selection, we instantiate one of three LangChain classes:
1.  **`RecursiveCharacterTextSplitter`**: The default and most robust. Uses `["\n\n", "\n", " ", ""]` as separators.
2.  **`CharacterTextSplitter`**: Simple split by `\n\n`.
3.  **`TokenTextSplitter`**: Splits by token count using `tiktoken`.

### F. Visualization & Stats Loop
Once chunks are generated:
1.  **Stats Calculation:** We calculate Max/Min/Avg characters and tokens.
2.  **Graph:** A bar chart (`st.bar_chart`) visualizes the length distribution.
3.  **Rendering Loop:** We iterate through each chunk to display it.
    *   **Color Cycling:** We cycle through a list of pastel colors to visually distinguish adjacent chunks.
    *   **Overlap Detection:** We algorithmically check the end of `chunk[i]` against the start of `chunk[i+1]` to identify the exact overlapping text.
    *   **Search Highlighting:** We check if the search term exists in the chunk and wrap it in a `<span style="background-color: yellow">` tag.
    *   **HTML Escaping:** We run `html.escape()` on *everything* before rendering to ensure safety.

---

## 4. Key Implementation Details for Presentation

*   **Robustness:** Mention the **Error Handling** for PDFs (using `try-except` blocks) and **HTML Escaping** to prevent app crashes from weird characters.
*   **Performance:** Mention **Session State** optimization. We don't re-run the heavy splitting logic when the user is just searching or scrolling; we only re-run when parameters change.
*   **Interactivity:** The app isn't just static; it provides real-time feedback (graphs, stats, highlighting) which makes it an excellent educational tool.
