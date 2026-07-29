import pandas as pd
import plotly.express as px
import re

def compute_doc_stats(text: str) -> dict:
    """
    Computes global statistics for the original document.
    """
    if not text:
        return {"char_count": 0, "word_count": 0}
    # Count words using simple regex split on whitespace
    words = re.findall(r'\b\w+\b', text)
    return {
        "char_count": len(text),
        "word_count": len(words)
    }

def compute_chunk_stats(chunks: list[dict], original_text: str) -> dict:
    """
    Computes statistics across all generated chunks.
    """
    if not chunks:
        return {
            "total_chunks": 0,
            "avg_length": 0.0,
            "max_length": 0,
            "min_length": 0,
            "avg_words": 0.0,
            "distribution_df": pd.DataFrame()
        }
        
    lengths = [len(c["text"]) for c in chunks]
    word_counts = [len(re.findall(r'\b\w+\b', c["text"])) for c in chunks]
    
    df = pd.DataFrame({
        "Chunk Index": list(range(1, len(chunks) + 1)),
        "Character Length": lengths,
        "Word Count": word_counts
    })
    
    return {
        "total_chunks": len(chunks),
        "avg_length": sum(lengths) / len(lengths),
        "max_length": max(lengths),
        "min_length": min(lengths),
        "avg_words": sum(word_counts) / len(word_counts),
        "distribution_df": df
    }

def generate_distribution_chart(df: pd.DataFrame, theme_dark: bool = False):
    """
    Generates a Plotly bar chart showing chunk sizes.
    """
    if df.empty:
        return None
        
    template = "plotly_dark" if theme_dark else "plotly_white"
    
    fig = px.bar(
        df,
        x="Chunk Index",
        y="Character Length",
        text="Character Length",
        title="Length of Each Chunk (Characters)",
        labels={"Character Length": "Length (chars)", "Chunk Index": "Chunk #"},
        color="Character Length",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        template=template,
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        height=300,
        coloraxis_showscale=False
    )
    fig.update_traces(textposition="outside")
    
    return fig
