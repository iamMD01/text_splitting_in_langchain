# Application Workflow Diagram

This document illustrates the data flow and logic of the Text Splitter Visualizer application.

```mermaid
graph TD
    User([User]) --> Input{Input Method}
    
    %% Input Stage
    Input -->|Paste Text| TextInput[Text Area]
    Input -->|Upload PDF| PDFLoader[PyPDFLoader]
    PDFLoader -->|Extracted Text| CleanText[Text Cleaning]
    TextInput --> CleanText
    
    %% Configuration Stage
    subgraph Sidebar [Sidebar Config]
        SplitterType{Select Splitter}
        Params[Set Parameters]
        Params -->|Chunk Size| Config
        Params -->|Overlap| Config
    end
    
    CleanText --> Button{Process Button Clicked?}
    Sidebar --> Button
    
    %% Processing Stage (LangChain)
    Button -->|Yes| SplitterEngine[LangChain Splitter Engine]
    
    subgraph SplitterLogic [Splitting Algorithms]
        SplitterEngine -->|Recursive| Recursive[RecursiveCharacterTextSplitter]
        SplitterEngine -->|Character| CharSplit[CharacterTextSplitter]
        SplitterEngine -->|Token| TokenSplit[TokenTextSplitter]
    end
    
    %% Output Stage
    Recursive --> Chunks[Generated Chunks List]
    CharSplit --> Chunks
    TokenSplit --> Chunks
    
    Chunks --> SessionState[(st.session_state)]
    
    %% Visualization Stage
    SessionState --> Stats[Calculate Stats]
    Stats -->|Max/Min/Avg| Metrics[Display Metrics]
    Stats -->|Token Counts| TokenMetrics[Tiktoken Analysis]
    
    SessionState --> Graph[Bar Chart Distribution]
    
    %% Rendering Loop
    SessionState --> RenderLoop[Chunk Rendering Loop]
    RenderLoop -->|Assign Color| VisualChunk[Visual Output Block]
    RenderLoop -->|Highlight Overlap| OverlapHighlight[Overlap Spans]
    RenderLoop -->|Search Query| SearchHighlight[Search Spans]
    
    %% Final View
    Metrics --> FinalView[Streamlit UI]
    TokenMetrics --> FinalView
    Graph --> FinalView
    VisualChunk --> FinalView
```

## Explanation
1.  **Input:** User provides text via direct input or PDF upload.
2.  **Config:** User selects the splitter type and parameters (size, overlap).
3.  **Processing:** On button click, the app uses LangChain to split the text based on the selected configuration.
4.  **State:** The resulting chunks are stored in `st.session_state` to persist across interactions (like searching).
5.  **Visualization:** The app calculates statistics, generates a distribution graph, and renders each chunk with color-coding and overlap highlighting.
