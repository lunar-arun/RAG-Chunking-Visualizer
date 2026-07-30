# 📚 RAG Chunking Visualizer

An interactive **Streamlit** application that helps you understand and compare different text chunking strategies used in **Retrieval-Augmented Generation (RAG)**. Experiment with various chunking methods, adjust parameters in real time, and visualize how text is split into chunks for downstream retrieval tasks.

## 🚀 Live Demo

Try the deployed application here:

**https://rag-chunking-visualizer-lunar.streamlit.app/**

## 📌 Overview

Chunking is one of the most important steps in building an effective RAG pipeline. Different chunking strategies can significantly impact retrieval quality, context preservation, and overall LLM performance.

This application provides an interactive playground to explore how different chunking techniques work, making it easier to understand their strengths, trade-offs, and ideal use cases.

## ✨ Features

### 📖 Theory

Learn the fundamentals of text chunking, including:

- Character Chunking
- Recursive Character Chunking
- Token Chunking
- Sentence Chunking
- Paragraph Chunking
- Fixed-Size Chunking
- Sliding Window Chunking
- Semantic Chunking

Each section includes:
- Explanation of how the method works
- Advantages and disadvantages
- Best use cases
- Simple examples

### 🎮 Interactive Playground

Experiment with chunking techniques in real time.

Features include:

- Select from multiple chunking strategies
- Configure chunk size and overlap
- Customize separators and token encodings
- Adjust semantic chunking thresholds
- Compare different chunking behaviors instantly

### 📊 Visualizations & Analytics

The app provides multiple ways to inspect generated chunks:

- Inline highlighted chunk visualization
- Individual chunk cards
- Overlap highlighting between chunks
- Chunk size distribution charts (Plotly)
- Document statistics including:
  - Total characters
  - Total words
  - Number of chunks
  - Average chunk size
  - Minimum and maximum chunk lengths

## 🛠️ Tech Stack

- Python
- Streamlit
- Plotly
- NLTK
- Tiktoken
- Scikit-learn
- TF-IDF & Cosine Similarity

## 📂 Project Structure

```text
chunking_visualizer/
│
├── app.py                     # Streamlit application entry point
│
├── pages/
│   ├── theory.py              # Theory page
│   └── playground.py          # Interactive playground
│
├── chunkers/
│   ├── character.py
│   ├── recursive.py
│   ├── token.py
│   ├── sentence.py
│   ├── paragraph.py
│   ├── sliding.py
│   └── semantic.py
│
├── utils/
│   ├── helpers.py
│   ├── statistics.py
│   └── visualization.py
│
├── requirements.txt
└── README.md
```

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch the Streamlit application

```bash
streamlit run app.py
```

The application will start locally and can typically be accessed at:

```
http://localhost:8501
```

## 📖 Usage

1. Launch the application.
2. Navigate to the **Theory** page to learn about chunking methods.
3. Open the **Playground** page.
4. Enter or paste your own text.
5. Select a chunking strategy.
6. Adjust the available parameters.
7. Explore the generated chunks and visualizations.

## 🎯 Purpose

This project is designed for developers, students, and AI practitioners who want to better understand how chunking affects retrieval performance in modern RAG systems. It serves as both a learning resource and an experimentation tool for comparing different chunking strategies.

## 📄 License

This project is available for educational and learning purposes.
