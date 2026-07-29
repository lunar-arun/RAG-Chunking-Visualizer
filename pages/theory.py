import streamlit as st

# Setup page style and layout
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');

/* Apply font globally */
.main .block-container {
    font-family: 'Inter', sans-serif;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* Custom cards */
.theory-card {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(128, 128, 128, 0.1);
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    transition: transform 0.2s, border-color 0.2s;
}
.theory-card:hover {
    transform: translateY(-2px);
    border-color: rgba(137, 88, 255, 0.4);
}

.gradient-text {
    background: linear-gradient(135deg, #8958FF 0%, #12D8FA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

.tag {
    background: rgba(137, 88, 255, 0.15);
    color: #8958FF;
    border: 1px solid rgba(137, 88, 255, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 12px;
}

/* Grid layout for cards */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.pro-box {
    border-left: 4px solid #10B981;
    background-color: rgba(16, 185, 129, 0.05);
    padding: 10px 15px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 10px;
}

.con-box {
    border-left: 4px solid #EF4444;
    background-color: rgba(239, 68, 68, 0.05);
    padding: 10px 15px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1>📖 RAG Chunking <span class='gradient-text'>Theory Guide</span></h1>", unsafe_allow_html=True)
st.markdown(
    "Chunking is the process of breaking down large documents into smaller, cohesive units of text "
    "before generating vector representations (embeddings). It is one of the most critical hyper-parameters "
    "when building reliable Retrieval-Augmented Generation (RAG) applications."
)

st.write("---")

# Core Concepts
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="theory-card">
        <h3>💡 What is Chunking?</h3>
        <p>In Large Language Model (LLM) pipelines, source documents (like PDFs, HTML articles, or Markdown files) are often far too large to fit comfortably inside a single embedding or context window.</p>
        <p><b>Chunking</b> involves slicing the document into smaller sub-documents (chunks). Each chunk is converted into an embedding vector and stored in a vector database for semantic search.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="theory-card">
        <h3>⚡ Why is Chunking Critical in RAG?</h3>
        <ul>
            <li><b>Retrieval Precision:</b> Smaller chunks contain specific facts, making similarity search more targeted.</li>
            <li><b>Context Limits:</b> LLMs have maximum context windows (e.g. 8k, 32k, or 128k tokens) and perform poorly if flooded with irrelevant filler text.</li>
            <li><b>Cost & Speed:</b> Smaller prompts reduce API billing and decrease response latency (Time to First Token).</li>
            <li><b>Hallucination Reduction:</b> Grounding the answer on highly focused segments minimizes LLM confusion.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Deep Dive into Techniques
st.markdown("## 🔍 Chunking Techniques Deep Dive")

# Tabs for each technique
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Character",
    "Recursive Character",
    "Token",
    "Sentence",
    "Paragraph",
    "Fixed Size",
    "Sliding Window",
    "Semantic"
])

with tab1:
    st.markdown("<span class='tag'>Standard Slicing</span>", unsafe_allow_html=True)
    st.markdown("### Character Chunking")
    st.write(
        "Character chunking is the simplest form of splitting. It splits text strictly by a static "
        "character count, optionally maintaining a fixed overlap to prevent information loss at the boundaries."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Extremely easy to understand and implement.<br>
            • Computationally trivial with zero dependencies.<br>
            • Ensures a uniform size across all vectors.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Completely ignores semantics, sentences, and word boundaries.<br>
            • Can cut a word in half, creating garbage tokens for the model.<br>
            • Highly prone to splitting crucial context.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Chunk Size:** The exact maximum number of characters that a single text chunk can contain.
    - **Overlap Size:** The number of characters that should be shared/duplicated between two adjacent chunks to maintain context at boundaries.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Ideal for simple, unstructured logs or flat files where structure does not carry meaning.")

    st.markdown("#### Example")
    st.code("Text: 'Retrieval Augmented Generation'\nChunk Size: 10, Overlap: 2\n-> Chunk 1: 'Retrieval '\n-> Chunk 2: 'al Augment'\n-> Chunk 3: 'ented Gene'", language="text")

with tab2:
    st.markdown("<span class='tag'>Highly Recommended</span>", unsafe_allow_html=True)
    st.markdown("### Recursive Character Chunking")
    st.write(
        "This is the default splitter in LangChain. It uses a list of separators (typically `[\"\\n\\n\", \"\\n\", \" \", \"\"]`) "
        "and recursively attempts to split the text. It aims to keep paragraphs, sentences, and words intact in that order "
        "of priority, ensuring chunks are as close to `chunk_size` as possible."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Respects text structures (paragraphs and sentences remain whole).<br>
            • Highly customizable through different separators.<br>
            • Best general-purpose splitter for standard prose and articles.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Relies on static formatting cues (newlines, spaces).<br>
            • Slower than simple character chunking.<br>
            • Still does not understand the semantic flow of text.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Chunk Size:** The maximum target character count for each merged text chunk.
    - **Overlap Size:** The maximum character overlap between adjacent finalized chunks.
    - **Separators:** A list of strings (e.g. `\\n\\n, \\n, " ", ""`) sorted by priority. The algorithm attempts to split at these points sequentially to avoid cutting sentences or words.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Default choice for documents, textbooks, PDFs, and standard markdown articles.")

    st.markdown("#### Example")
    st.code("Separators: ['\\n\\n', '\\n', ' ', '']\nIt first tries to split by paragraphs. If a paragraph is > chunk_size, it splits it by lines. If a line is still > chunk_size, it splits by words.", language="text")

with tab3:
    st.markdown("<span class='tag'>LLM Native</span>", unsafe_allow_html=True)
    st.markdown("### Token Chunking")
    st.write(
        "Since Large Language Models process text in tokens rather than characters or words, "
        "Token Chunking splits the text based on token count. It uses an encoder (like `tiktoken` "
        "for OpenAI models) to count and segment tokens."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Ensures chunks never exceed the model's token constraints.<br>
            • Maximizes the context window utilization.<br>
            • Prevents tokenization bugs.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Indecipherable to human readers in raw token formats.<br>
            • Requires tokenization libraries (tiktoken, transformers).<br>
            • Decoded character sizes are unpredictable (e.g. non-English text uses more tokens).
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Chunk Size:** The maximum target token count for each chunk.
    - **Overlap Size:** The number of shared tokens between adjacent chunks.
    - **Encoding Model:** The vocabulary mapping (e.g. `cl100k_base` for GPT-4/3.5) used to convert characters to integer tokens.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("RAG pipelines targeting OpenAI models or open-weights LLMs where strict token budgeting is required.")

    st.markdown("#### Example")
    st.code("Encoding: cl100k_base\nChunk Size: 3 tokens, Overlap: 1 token\nInput: 'Retrieval Augmented Generation'\n-> Tokens: [23508, 45293, 12053]\n-> Chunk 1: 'Retrieval Augmented' (2 tokens)\n-> Chunk 2: 'Augmented Generation' (2 tokens)", language="text")

with tab4:
    st.markdown("<span class='tag'>Grammar Aware</span>", unsafe_allow_html=True)
    st.markdown("### Sentence Chunking")
    st.write(
        "Sentence chunking splits the document into natural sentences. It uses grammatical rules (like those "
        "provided by `nltk` or `spaCy`) to recognize punctuation and structure, guaranteeing that every "
        "chunk represents a complete grammatical statement."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Preserves full complete thoughts and logical statements.<br>
            • Highly readable and clean chunks.<br>
            • Excellent for answering specific, fact-based questions.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Chunks vary drastically in size (short sentences vs long sentences).<br>
            • Single sentences may lack broader context (e.g., pronouns like 'He' or 'It' refer to previous sentences).<br>
            • Requires grammatical tokenizer downloads.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - *No parameters:* Splits text strictly at natural sentence boundaries detected by standard punctuation.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Question-answering bots dealing with dense facts, legal documents, or customer reviews.")

    st.markdown("#### Example")
    st.code("Sentence 1: 'RAG retrieves facts.'\nSentence 2: 'Then it grounds the model.'\n-> Chunk 1: 'RAG retrieves facts.'\n-> Chunk 2: 'Then it grounds the model.'", language="text")

with tab5:
    st.markdown("<span class='tag'>Structure Aware</span>", unsafe_allow_html=True)
    st.markdown("### Paragraph Chunking")
    st.write(
        "Paragraph chunking splits text by paragraph breaks (usually double newlines `\\n\\n`). "
        "It presumes that authors write paragraphs as standalone, single-topic segments, which naturally "
        "keeps semantic themes grouped together."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Excellent semantic coherence, as writers structure thoughts by paragraphs.<br>
            • Simple to implement (split by double newlines).<br>
            • Keeps lists, tables, or sections grouped.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Heavily dependent on the quality of document formatting.<br>
            • Paragraphs can be extremely long or extremely short, leading to unbalanced embeddings.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - *No parameters:* Splits text strictly at paragraph separations (`\\n\\n`).
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Novels, news articles, academic papers, and essays where paragraphs are cohesive.")

with tab6:
    st.markdown("<span class='tag'>Strict Uniformity</span>", unsafe_allow_html=True)
    st.markdown("### Fixed Size Chunking")
    st.write(
        "Fixed Size chunking slices the document into chunks of an exact character size, without "
        "looking at separators or word boundaries. There is no overlap, resulting in hard boundaries."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Guarantees 100% uniform chunk size.<br>
            • Easiest to store in database arrays.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Severely damages semantic structure.<br>
            • Breaks sentences, punctuation, and words arbitrarily.<br>
            • Worst choice for semantic search quality.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Chunk Size:** The exact character length for every single chunk. No overlaps are calculated.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Rarely used in production; serves as a baseline comparison for chunking research.")

with tab7:
    st.markdown("<span class='tag'>Redundant Coverage</span>", unsafe_allow_html=True)
    st.markdown("### Sliding Window Chunking")
    st.write(
        "Sliding window chunking slides a window of fixed size (characters or tokens) across the text "
        "by a specified slide step. When the step is smaller than the window, adjacent chunks have "
        "significant overlap. This ensures that whatever information is split at a boundary is fully captured "
        "by the next chunk."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Prevents information loss at boundaries.<br>
            • Provides redundant context, making retrieval more forgiving.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Leads to highly redundant database vectors (high storage cost).<br>
            • Increased API billing because the same sentences are embedded multiple times.<br>
            • Can return highly repetitive results.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Sliding Unit:** Operates either on *Characters* or *Tokens*.
    - **Window Size:** The maximum viewport length (in characters or tokens) per chunk.
    - **Slide Step Size:** The stride or index shift for each subsequent window. The overlap equals `Window Size - Slide Step Size`.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Highly critical knowledge retrieval where boundary cutoffs could lead to complete RAG failure.")

with tab8:
    st.markdown("<span class='tag'>AI & Math Driven</span>", unsafe_allow_html=True)
    st.markdown("### Semantic Chunking")
    st.write(
        "Semantic chunking splits the document based on content similarity rather than structure. "
        "It splits the text into sentences, measures the semantic distance (or similarity) between "
        "consecutive sentences, and places boundaries where similarity drops significantly."
    )
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="pro-box">
            <b>Advantages:</b><br>
            • Truly groups similar ideas together regardless of document format.<br>
            • Adapts dynamically to changes in text topics.<br>
            • Produces the highest-quality retrieval performance.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="con-box">
            <b>Disadvantages:</b><br>
            • Computationally heavy (requires sentence embeddings or TF-IDF matrix calculations).<br>
            • Difficult to fine-tune (requires setting similarity thresholds).<br>
            • Chunk sizes are unpredictable.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("#### ⚙️ Parameters Explained")
    st.markdown("""
    - **Threshold Type:** Sets the logic for split boundaries:
      - *Percentile:* Splits at points where semantic similarity is below a specific percentile (e.g. the lowest 30%).
      - *Absolute:* Splits where similarity drops below a hard cosine similarity decimal (e.g. 0.3).
    - **Threshold Value:** The percentile value (5-95) or the absolute similarity threshold (0.0-1.0).
    - **Min Sentences per Chunk:** The minimum number of sentences that must be grouped together before a split is allowed.
    """)
    
    st.markdown("#### Best Use Case")
    st.write("Complex, long-form documents containing multiple topics or shifts in conversation (e.g. meeting transcripts, legal contracts).")
