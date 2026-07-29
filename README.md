# RAG Chunking Visualizer

An interactive and educational **Streamlit web application** that visualizes different text chunking techniques for Retrieval-Augmented Generation (RAG). Users can input text, configure parameters, and immediately see how text is split into chunks with visualizations similar to ChunkViz.

---

## Features

### 📖 Theory Page
- Explains what chunking is and why it is critical in RAG pipelines.
- Explains character, recursive, token, sentence, paragraph, fixed-size, sliding-window, and semantic chunking mechanisms.
- Covers advantages, disadvantages, best use cases, and simple examples for each method.

### 🎮 Playground Page
- **Interactive Controls:** Select any chunking technique and configure parameters dynamically (e.g. Chunk Size, Overlap Size, Separators, Token Encodings, Semantic Percentiles).
- **Multiple Chunk Visualizations:**
  - **Inline Highlight Mode:** Alternating pastel highlights across the entire document.
  - **Chunk Card Mode:** Separate cards for each chunk with overlapping text highlighted in **bold** to immediately show context duplication.
- **Document-Wide Analytics:** Total characters, words, average/max/min chunk sizes, and a Plotly distribution chart.

---

## Project Structure

```
chunking_visualizer/
│
├── app.py                     # App entrypoint (st.navigation setup)
│
├── pages/
│   ├── theory.py              # Theory explanation page
│   └── playground.py          # Playground UI and visualizer columns
│
├── chunkers/
│   ├── __init__.py            # Module exports
│   ├── character.py           # Character-level chunker
│   ├── recursive.py           # Recursive character-level chunker
│   ├── token.py               # Token-based chunker (using tiktoken)
│   ├── sentence.py            # Sentence-based chunker (using NLTK/regex)
│   ├── paragraph.py           # Paragraph-based chunker (split on \n\n)
│   ├── sliding.py             # Sliding window chunker
│   └── semantic.py            # TF-IDF Cosine Similarity semantic chunker
│
├── utils/
│   ├── __init__.py            # Module exports
│   ├── helpers.py             # Default sample texts
│   ├── statistics.py          # Analytical metrics and charts
│   └── visualization.py       # HSL palette, overlap bolding, and HTML renderer
│
└── requirements.txt           # Project dependencies
```

---

## How to Run

1. **Activate the Virtual Environment:**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Application:**
   ```bash
   streamlit run app.py
   ```
