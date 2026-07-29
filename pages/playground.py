import streamlit as st
import chunkers
import utils

# Ensure sidebar is collapsed on load
if st.session_state.get("sidebar_state") != "collapsed":
    st.session_state.sidebar_state = "collapsed"
    st.rerun()

# Apply page custom styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&display=swap');

.main .block-container {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
}

.gradient-title {
    background: linear-gradient(135deg, #FF6B6B 0%, #8958FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Styled control cards */
.control-section {
    background-color: rgba(0, 0, 0, 0.02);
    border: 1px solid rgba(0, 0, 0, 0.08);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}

/* Chunk Card Styling */
.chunk-card {
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 15px;
    border-left: 5px solid;
    transition: all 0.2s;
}
.chunk-card:hover {
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transform: translateX(2px);
}

.chunk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 0.9rem;
    font-weight: 600;
}

.chunk-body {
    font-size: 0.95rem;
    line-height: 1.6;
    white-space: pre-wrap;
}

/* Stat Box style */
.stat-item {
    padding: 10px;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid rgba(0, 0, 0, 0.05);
    text-align: center;
}

.stat-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: #6E38F0;
}

.stat-lbl {
    font-size: 0.8rem;
    color: #666666;
}

/* Empty state style */
.empty-state {
    text-align: center;
    padding: 40px;
    border: 2px dashed rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    color: #666666;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎮 Chunking <span class='gradient-title'>Playground</span></h1>", unsafe_allow_html=True)

# ----------------- SESSION STATE INIT -----------------
if "text_area_input" not in st.session_state:
    st.session_state.text_area_input = ""
if "processed" not in st.session_state:
    st.session_state.processed = False
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "tech_idx" not in st.session_state:
    st.session_state.tech_idx = 1 # default to Recursive Character Chunking
if "last_processed_text" not in st.session_state:
    st.session_state.last_processed_text = ""

# Initialize synchronized parameters
if "chunk_size" not in st.session_state:
    st.session_state.chunk_size = 250
if "overlap" not in st.session_state:
    st.session_state.overlap = 50
if "window_size" not in st.session_state:
    st.session_state.window_size = 250
if "step_size" not in st.session_state:
    st.session_state.step_size = 100

# Separators parser helper
def parse_separators(input_str: str) -> list[str]:
    raw_seps = [s.strip() for s in input_str.split(",")]
    parsed = []
    for s in raw_seps:
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        s = s.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
        parsed.append(s)
    return parsed

# Callback: Load sample text
def load_sample():
    if st.session_state.sample_select != "Select a sample...":
        sample_text = utils.get_sample_text(st.session_state.sample_select)
        st.session_state.text_area_input = sample_text
        st.session_state.processed = False

# Callback: Reset fields
def reset_fields():
    st.session_state.text_area_input = ""
    st.session_state.last_processed_text = ""
    st.session_state.processed = False
    st.session_state.chunks = []
    st.session_state.sample_select = "Select a sample..."
    st.session_state.tech_idx = 1
    
    # Reset synchronized parameters
    st.session_state.chunk_size = 250
    st.session_state.overlap = 50
    st.session_state.window_size = 250
    st.session_state.step_size = 100
    
    # reset widget keys by deletion (streamlit recreates them on next run)
    keys_to_clear = [
        "chunk_size_slide_widget", "chunk_size_num_widget",
        "overlap_slide_widget", "overlap_num_widget",
        "window_size_slide_widget", "window_size_num_widget",
        "step_size_slide_widget", "step_size_num_widget",
        "separators", "encoding_name", "sliding_unit",
        "semantic_threshold_type", "semantic_threshold_value", "min_sentences"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Synchronizer callbacks
def sync_chunk_size_slide():
    st.session_state.chunk_size = st.session_state.chunk_size_slide_widget
    st.session_state.processed = False

def sync_chunk_size_num():
    st.session_state.chunk_size = st.session_state.chunk_size_num_widget
    st.session_state.processed = False

def sync_overlap_slide():
    st.session_state.overlap = st.session_state.overlap_slide_widget
    st.session_state.processed = False

def sync_overlap_num():
    st.session_state.overlap = st.session_state.overlap_num_widget
    st.session_state.processed = False

def sync_window_size_slide():
    st.session_state.window_size = st.session_state.window_size_slide_widget
    st.session_state.processed = False

def sync_window_size_num():
    st.session_state.window_size = st.session_state.window_size_num_widget
    st.session_state.processed = False

def sync_step_size_slide():
    st.session_state.step_size = st.session_state.step_size_slide_widget
    st.session_state.processed = False

def sync_step_size_num():
    st.session_state.step_size = st.session_state.step_size_num_widget
    st.session_state.processed = False

# ----------------- MAIN COLUMNS -----------------
col_ctrl, col_vis = st.columns([5, 7], gap="large")

with col_ctrl:
    st.markdown("### 🛠️ Controls")
    
    # 1. Sample Selector
    st.selectbox(
        "Load Sample Text",
        ["Select a sample...", "RAG & Information Retrieval", "The Story of the Golden Gate Bridge", "Technical Documentation Example"],
        key="sample_select",
        on_change=load_sample
    )
    
    # 2. Technique Selector
    techniques = [
        "Character Chunking",
        "Recursive Character Chunking",
        "Token Chunking",
        "Sentence Chunking",
        "Paragraph Chunking",
        "Fixed Size Chunking",
        "Sliding Window Chunking",
        "Semantic Chunking"
    ]
    
    selected_technique = st.selectbox(
        "Select Chunking Technique",
        techniques,
        index=st.session_state.tech_idx,
        key="technique_select"
    )
    
    # Track selection changes
    current_tech_idx = techniques.index(selected_technique)
    if current_tech_idx != st.session_state.tech_idx:
        st.session_state.tech_idx = current_tech_idx
        st.session_state.processed = False
        
    st.write("")
    
    # 3. Dynamic Parameters
    st.markdown("#### ⚙️ Parameters")
    params = {}
    
    if selected_technique in ["Character Chunking", "Recursive Character Chunking", "Token Chunking"]:
        # Synchronized Chunk Size Slider + Number Input
        st.slider("Chunk Size", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_slide_widget", on_change=sync_chunk_size_slide)
        st.number_input("Enter Chunk Size value", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_num_widget", on_change=sync_chunk_size_num)
        params["chunk_size"] = st.session_state.chunk_size
        
        # Synchronized Overlap Size Slider + Number Input
        st.slider("Overlap Size", min_value=0, max_value=1000, value=st.session_state.overlap, step=5, key="overlap_slide_widget", on_change=sync_overlap_slide)
        st.number_input("Enter Overlap Size value", min_value=0, max_value=1000, value=st.session_state.overlap, step=5, key="overlap_num_widget", on_change=sync_overlap_num)
        params["overlap"] = st.session_state.overlap
        
        # Additional configs
        if selected_technique == "Recursive Character Chunking":
            params["separators"] = st.text_input("Separators (comma separated)", '\\n\\n, \\n, " ", ""', key="separators")
        elif selected_technique == "Token Chunking":
            params["encoding_name"] = st.selectbox("Encoding Model", ["cl100k_base", "p50k_base", "r50k_base"], key="encoding_name")
            
    elif selected_technique == "Fixed Size Chunking":
        # Synchronized Chunk Size Slider + Number Input
        st.slider("Chunk Size", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_slide_widget", on_change=sync_chunk_size_slide)
        st.number_input("Enter Chunk Size value", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_num_widget", on_change=sync_chunk_size_num)
        params["chunk_size"] = st.session_state.chunk_size
        
    elif selected_technique == "Sliding Window Chunking":
        sliding_unit = st.radio("Sliding Unit", ["Characters", "Tokens"], key="sliding_unit")
        params["use_tokens"] = (sliding_unit == "Tokens")
        
        # Synchronized Window Size Slider + Number Input
        st.slider("Window Size", min_value=10, max_value=2000, value=st.session_state.window_size, step=10, key="window_size_slide_widget", on_change=sync_window_size_slide)
        st.number_input("Enter Window Size value", min_value=10, max_value=2000, value=st.session_state.window_size, step=10, key="window_size_num_widget", on_change=sync_window_size_num)
        params["window_size"] = st.session_state.window_size
        
        # Synchronized Slide Step Slider + Number Input
        st.slider("Slide Step Size", min_value=5, max_value=1000, value=st.session_state.step_size, step=5, key="step_size_slide_widget", on_change=sync_step_size_slide)
        st.number_input("Enter Slide Step Size value", min_value=5, max_value=1000, value=st.session_state.step_size, step=5, key="step_size_num_widget", on_change=sync_step_size_num)
        params["step_size"] = st.session_state.step_size
        
    elif selected_technique == "Semantic Chunking":
        params["threshold_type"] = st.radio("Threshold Type", ["percentile", "absolute"], format_func=lambda x: x.capitalize(), key="semantic_threshold_type")
        if params["threshold_type"] == "percentile":
            params["threshold_value"] = st.slider("Percentile Cutoff (lower values split less)", min_value=5, max_value=95, value=30, step=5, key="semantic_threshold_value")
        else:
            params["threshold_value"] = st.slider("Absolute Similarity Threshold (lower splits less)", min_value=0.0, max_value=1.0, value=0.3, step=0.05, key="semantic_threshold_value")
        params["min_sentences"] = st.number_input("Min Sentences per Chunk", min_value=1, max_value=10, value=1, key="min_sentences")
        
    st.write("")
    
    # 4. Text Input
    st.text_area(
        "Paste your text here...",
        value=st.session_state.text_area_input,
        height=280,
        key="text_area_input"
    )
    
    # If the text in the text area is edited and differs from what we processed, mark processed = False
    if st.session_state.text_area_input != st.session_state.last_processed_text:
        st.session_state.processed = False

    # 5. Buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        process_clicked = st.button("🚀 Process", use_container_width=True, type="primary")
    with btn_col2:
        reset_clicked = st.button("🧹 Reset", use_container_width=True, on_click=reset_fields)

    # 6. Process Action
    if process_clicked:
        if not st.session_state.text_area_input.strip():
            st.error("Please enter or load some text first.")
        else:
            # Run Chunker
            txt = st.session_state.text_area_input
            st.session_state.last_processed_text = txt
            with st.spinner("Processing chunks..."):
                if selected_technique == "Character Chunking":
                    st.session_state.chunks = chunkers.chunk_character(
                        txt, params["chunk_size"], params["overlap"]
                    )
                elif selected_technique == "Recursive Character Chunking":
                    seps = parse_separators(params["separators"])
                    st.session_state.chunks = chunkers.chunk_recursive(
                        txt, params["chunk_size"], params["overlap"], seps
                    )
                elif selected_technique == "Token Chunking":
                    st.session_state.chunks = chunkers.chunk_token(
                        txt, params["chunk_size"], params["overlap"], params["encoding_name"]
                    )
                elif selected_technique == "Sentence Chunking":
                    st.session_state.chunks = chunkers.chunk_sentence(txt)
                elif selected_technique == "Paragraph Chunking":
                    st.session_state.chunks = chunkers.chunk_paragraph(txt)
                elif selected_technique == "Fixed Size Chunking":
                    st.session_state.chunks = chunkers.chunk_character(
                        txt, params["chunk_size"], 0
                    )
                elif selected_technique == "Sliding Window Chunking":
                    st.session_state.chunks = chunkers.chunk_sliding_window(
                        txt, params["window_size"], params["step_size"], params["use_tokens"]
                    )
                elif selected_technique == "Semantic Chunking":
                    st.session_state.chunks = chunkers.chunk_semantic(
                        txt, params["threshold_type"], params["threshold_value"], params["min_sentences"]
                    )
                
                st.session_state.processed = True
                st.rerun()

# ----------------- RIGHT COLUMN (VISUALIZATION) -----------------
with col_vis:
    st.markdown("### 📊 Visualization & Analysis")
    
    if st.session_state.processed and st.session_state.chunks:
        chunks = st.session_state.chunks
        txt = st.session_state.text_area_input
        
        # 1. Selected Method Details
        c_size_str = str(params.get("chunk_size", params.get("window_size", "N/A")))
        c_overlap_str = str(params.get("overlap", params.get("window_size", 0) - params.get("step_size", 0) if "step_size" in params else "N/A"))
        if selected_technique in ["Sentence Chunking", "Paragraph Chunking", "Semantic Chunking"]:
            c_overlap_str = "Dynamic"
            if selected_technique != "Semantic Chunking":
                c_size_str = "Dynamic"
            else:
                c_size_str = f"Dynamic (TF-IDF Similarity: {params['threshold_value']})"
                
        st.markdown(f"""
        <div style="background-color: rgba(110, 56, 240, 0.05); border: 1px solid rgba(110, 56, 240, 0.2); padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem;">
            <b>Active Technique:</b> {selected_technique} &nbsp;|&nbsp; 
            <b>Target Size:</b> {c_size_str} &nbsp;|&nbsp; 
            <b>Overlap:</b> {c_overlap_str} &nbsp;|&nbsp; 
            <b>Chunks Created:</b> {len(chunks)}
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Toggle Advanced Inline Visualization
        show_inline = st.checkbox("☑ Show Inline Visualization (Alternating Highlights)", value=True)
        
        if show_inline:
            st.markdown("#### ⚡ Inline Document Highlights")
            inline_html = utils.build_inline_visualization_html(txt, chunks)
            st.markdown(inline_html, unsafe_allow_html=True)
            st.write("")
            
        # 3. Chunk Cards
        st.markdown("#### 📄 Chunk Cards")
        for k in range(len(chunks)):
            chunk = chunks[k]
            bg_color = utils.get_hsl_color(k, alpha=0.08)
            border_color = utils.get_hsl_border(k, alpha=0.35)
            
            # Formatted text with bold overlaps
            bolded_html_text = utils.format_chunk_text_with_bold_overlaps(chunks, k, is_html=True)
            
            # Word count and token count if available
            words_in_chunk = len(chunk["text"].split())
            tok_count_str = f" | {chunk['token_count']} tokens" if "token_count" in chunk else ""
            
            card_html = f"""
            <div class="chunk-card" style="background-color: {bg_color}; border-color: {border_color}; border-left-width: 5px;">
                <div class="chunk-header">
                    <span style="color: {border_color};">🟢 Chunk {k + 1}</span>
                    <span style="color: #666666; font-size: 0.8rem;">
                        Length: {len(chunk['text'])} chars | {words_in_chunk} words{tok_count_str} | Range: [{chunk['start_index']}:{chunk['end_index']}]
                    </span>
                </div>
                <div class="chunk-body">{bolded_html_text}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
    elif st.session_state.processed and not st.session_state.chunks:
        st.info("No chunks were generated. Please check your text input or parameters.")
    else:
        # Empty state visualizer
        st.markdown("""
        <div class="empty-state">
            <h1 style="font-size: 3rem; margin-bottom: 10px;">🎮</h1>
            <h3>Ready to split your documents?</h3>
            <p>1. Choose or paste a text document in the control panel.</p>
            <p>2. Select your desired chunking technique and configure parameters.</p>
            <p>3. Click <b>Process</b> to see the magic visualization!</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- FOOTER STATISTICS -----------------
st.write("---")
st.markdown("### 📈 Document-Wide Analytics")

if st.session_state.processed and st.session_state.chunks:
    chunks = st.session_state.chunks
    txt = st.session_state.text_area_input
    
    # Compute global & chunk statistics
    doc_stats = utils.compute_doc_stats(txt)
    chunk_stats = utils.compute_chunk_stats(chunks, txt)
    
    # Display statistics cards
    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    
    with sc1:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{doc_stats['char_count']}</div>
            <div class="stat-lbl">Total Characters</div>
        </div>
        """, unsafe_allow_html=True)
        
    with sc2:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{doc_stats['word_count']}</div>
            <div class="stat-lbl">Total Words</div>
        </div>
        """, unsafe_allow_html=True)
        
    with sc3:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{chunk_stats['total_chunks']}</div>
            <div class="stat-lbl">Total Chunks</div>
        </div>
        """, unsafe_allow_html=True)
        
    with sc4:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{chunk_stats['avg_length']:.0f}</div>
            <div class="stat-lbl">Avg Chunk Chars</div>
        </div>
        """, unsafe_allow_html=True)
        
    with sc5:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{chunk_stats['max_length']}</div>
            <div class="stat-lbl">Largest Chunk Chars</div>
        </div>
        """, unsafe_allow_html=True)
        
    with sc6:
        st.markdown(f"""
        <div class="stat-item">
            <div class="stat-val">{chunk_stats['min_length']}</div>
            <div class="stat-lbl">Smallest Chunk Chars</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Draw Plotly distribution chart (always light mode)
    fig = utils.generate_distribution_chart(chunk_stats["distribution_df"], theme_dark=False)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
else:
    # Empty stats placeholder
    sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
    for c in [sc1, sc2, sc3, sc4, sc5, sc6]:
        with c:
            st.markdown("""
            <div class="stat-item">
                <div class="stat-val">-</div>
                <div class="stat-lbl">N/A</div>
            </div>
            """, unsafe_allow_html=True)
