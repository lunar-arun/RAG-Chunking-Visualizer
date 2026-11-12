# 📚 RAG Chunking Visualizer

An interactive **Streamlit application** to explore and compare different text chunking strategies used in **Retrieval-Augmented Generation (RAG)**.

Experiment with chunking methods, customize parameters, and visualize how text is divided into chunks for better document retrieval.

## 🚀 Live Demo

**Try the RAG Chunking Visualizer**

## ✨ Features

- **Chunking Theory:** Understand different chunking techniques with explanations, advantages, limitations, and examples.
- **Interactive Playground:** Experiment with chunk sizes, overlap, separators, and semantic thresholds.
- **Multiple Strategies:**
  - Character Chunking
  - Recursive Character Chunking
  - Token Chunking
  - Sentence Chunking
  - Paragraph Chunking
  - Fixed-Size Chunking
  - Sliding Window Chunking
  - Semantic Chunking
- **Visualizations:** Explore highlighted chunks, overlapping text, and chunk size distribution charts.
- **Statistics:** Analyze character count, word count, number of chunks, and average, minimum, and maximum chunk sizes.

## 🛠️ Tech Stack

- Python
- Streamlit
- Plotly
- NLTK
- Tiktoken
- Scikit-learn
- TF-IDF & Cosine Similarity

## ⚙️ Run Locally

**1\. Clone the repository**

bash

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

**2\. Create and activate a virtual environment**

bash

```bash
python -m venv .venv
```

Windows:

bash

```bash
.venv\Scripts\activate
```

macOS / Linux:

bash

```bash
source .venv/bin/activate
```

**3\. Install dependencies**

bash

```bash
pip install -r requirements.txt
```

**4\. Start the application**

bash

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 🎯 Purpose

This project aims to simplify the understanding of text chunking techniques and demonstrate how different strategies influence context preservation and retrieval in RAG pipelines.

---

**Explore. Experiment. Visualize. Understand RAG Chunking\!**
