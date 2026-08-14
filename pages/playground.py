import streamlit as st
import chunkers
import utils

# Ensure sidebar is collapsed on load
if st.session_state.get("sidebar_state") != "collapsed":
    st.session_state.sidebar_state = "collapsed"
    st.rerun()

# Apply page-specific styles (layered on top of the shared theme in app.py)
st.markdown("""
<style>
/* Styled control cards */
.control-section {
    background-color: var(--bg-panel);
    border: 1px solid var(--border-color);
    padding: 20px;
    border-radius: var(--radius-md);
    margin-bottom: 15px;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

/* Live parameter summary badge */
.param-badge {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 6px 0 4px 0;
}
.param-chip {
    background: var(--bg-panel-alt);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-primary);
}
.param-chip b { color: var(--text-primary); font-family: 'Inter', sans-serif; font-weight: 500; }

/* Active technique summary bar */
.active-summary {
    background: linear-gradient(90deg, var(--accent-secondary-glow), var(--accent-primary-glow));
    border: 1px solid var(--border-color);
    padding: 12px 16px;
    border-radius: var(--radius-md);
    margin-bottom: 18px;
    font-size: 0.88rem;
    color: var(--text-primary);
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    animation: chunkFadeIn 0.3s ease;
}
.active-summary b { color: var(--accent-primary); }

/* Chunk navigation chips */
.chunk-nav-wrap { margin-bottom: 4px; }

/* Chunk Card Styling */
.chunk-card {
    border-radius: var(--radius-md);
    padding: 16px;
    margin-bottom: 14px;
    border-left: 5px solid;
    border-top: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    animation: chunkFadeIn 0.3s ease;
}
.chunk-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    transform: translateX(3px);
}
.chunk-card.selected {
    box-shadow: 0 0 0 1px var(--accent-primary), 0 0 24px var(--accent-primary-glow);
}

.chunk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 0.85rem;
    font-weight: 600;
}
.chunk-meta {
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
}

.chunk-body {
    font-size: 0.95rem;
    line-height: 1.65;
    white-space: pre-wrap;
    color: var(--text-primary);
    word-break: break-word;
}

.selected-badge {
    background: var(--accent-primary);
    color: #0B0F17;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 1px 8px;
    border-radius: 10px;
    margin-left: 8px;
    letter-spacing: 0.03em;
}

/* Chunk detail panel */
.detail-panel {
    background: var(--bg-panel);
    border: 1px solid var(--accent-primary);
    box-shadow: 0 0 24px var(--accent-primary-glow);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 18px;
    animation: chunkFadeIn 0.25s ease;
}
.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 10px;
    margin-top: 10px;
}
.detail-item .val { font-size: 1.15rem; font-weight: 700; color: var(--accent-primary); }
.detail-item .lbl { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }

/* Stat Box style */
.stat-item {
    padding: 12px 10px;
    border-radius: var(--radius-sm);
    background: var(--bg-panel);
    border: 1px solid var(--border-color);
    text-align: center;
    transition: border-color 0.15s ease;
}
.stat-item:hover {
    border-color: var(--accent-primary);
}

.stat-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-primary);
}

.stat-lbl {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* Empty state style */
.empty-state {
    text-align: center;
    padding: 48px 24px;
    border: 2px dashed var(--border-strong);
    border-radius: var(--radius-lg);
    color: var(--text-secondary);
    background: var(--bg-panel);
}
.empty-state h3 { color: var(--text-primary); }
.empty-state p { color: var(--text-secondary); margin: 4px 0; }

/* Error hint box */
.error-hint {
    background: rgba(248, 113, 113, 0.08);
    border: 1px solid rgba(248, 113, 113, 0.3);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 0.85rem;
    color: var(--text-primary);
    margin-top: 8px;
}

@keyframes chunkFadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 900px) {
    .chunk-header { flex-direction: column; align-items: flex-start; gap: 4px; }
    .detail-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎮 Chunking <span class='gradient-title'>Playground</span></h1>", unsafe_allow_html=True)
st.caption("Paste text, pick a technique, and watch exactly how your document gets split — hover or select any chunk to inspect it.")

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
if "selected_chunk_idx" not in st.session_state:
    st.session_state.selected_chunk_idx = None

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
    st.session_state.selected_chunk_idx = None
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
        st.session_state.selected_chunk_idx = None
        
    st.write("")
    
    # 3. Dynamic Parameters
    st.markdown("#### ⚙️ Parameters")
    params = {}
    
    if selected_technique in ["Character Chunking", "Recursive Character Chunking", "Token Chunking"]:
        # Synchronized Chunk Size Slider + Number Input
        st.slider("Chunk Size", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_slide_widget", on_change=sync_chunk_size_slide, help="Maximum size of each chunk. Larger chunks keep more context together but are less precise for retrieval.")
        st.number_input("Enter Chunk Size value", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_num_widget", on_change=sync_chunk_size_num)
        params["chunk_size"] = st.session_state.chunk_size
        
        # Synchronized Overlap Size Slider + Number Input
        st.slider("Overlap Size", min_value=0, max_value=1000, value=st.session_state.overlap, step=5, key="overlap_slide_widget", on_change=sync_overlap_slide, help="Characters shared between adjacent chunks, shown bolded in the visualization. Higher overlap reduces context loss at boundaries but increases redundancy.")
        st.number_input("Enter Overlap Size value", min_value=0, max_value=1000, value=st.session_state.overlap, step=5, key="overlap_num_widget", on_change=sync_overlap_num)
        params["overlap"] = st.session_state.overlap
        
        # Additional configs
        if selected_technique == "Recursive Character Chunking":
            params["separators"] = st.text_input("Separators (comma separated)", '\\n\\n, \\n, " ", ""', key="separators", help="Tried in order — paragraph breaks first, then lines, then spaces, then any character — to keep text intact as long as possible.")
        elif selected_technique == "Token Chunking":
            params["encoding_name"] = st.selectbox("Encoding Model", ["cl100k_base", "p50k_base", "r50k_base"], key="encoding_name", help="The tokenizer vocabulary used to count tokens, e.g. cl100k_base matches GPT-3.5/4.")
            
    elif selected_technique == "Fixed Size Chunking":
        # Synchronized Chunk Size Slider + Number Input
        st.slider("Chunk Size", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_slide_widget", on_change=sync_chunk_size_slide, help="Exact character length for every chunk. No overlap is applied.")
        st.number_input("Enter Chunk Size value", min_value=10, max_value=2000, value=st.session_state.chunk_size, step=10, key="chunk_size_num_widget", on_change=sync_chunk_size_num)
        params["chunk_size"] = st.session_state.chunk_size
        
    elif selected_technique == "Sliding Window Chunking":
        sliding_unit = st.radio("Sliding Unit", ["Characters", "Tokens"], key="sliding_unit", help="Whether the window and step are measured in characters or tokens.")
        params["use_tokens"] = (sliding_unit == "Tokens")
        
        # Synchronized Window Size Slider + Number Input
        st.slider("Window Size", min_value=10, max_value=2000, value=st.session_state.window_size, step=10, key="window_size_slide_widget", on_change=sync_window_size_slide, help="The length of each window/chunk.")
        st.number_input("Enter Window Size value", min_value=10, max_value=2000, value=st.session_state.window_size, step=10, key="window_size_num_widget", on_change=sync_window_size_num)
        params["window_size"] = st.session_state.window_size
        
        # Synchronized Slide Step Slider + Number Input
        st.slider("Slide Step Size", min_value=5, max_value=1000, value=st.session_state.step_size, step=5, key="step_size_slide_widget", on_change=sync_step_size_slide, help="How far the window moves forward each time. Overlap = Window Size − Slide Step Size.")
        st.number_input("Enter Slide Step Size value", min_value=5, max_value=1000, value=st.session_state.step_size, step=5, key="step_size_num_widget", on_change=sync_step_size_num)
        params["step_size"] = st.session_state.step_size
        
    elif selected_technique == "Semantic Chunking":
        params["threshold_type"] = st.radio("Threshold Type", ["percentile", "absolute"], format_func=lambda x: x.capitalize(), key="semantic_threshold_type", help="Percentile splits at the weakest X% of similarity gaps; Absolute splits wherever similarity drops below a fixed value.")
        if params["threshold_type"] == "percentile":
            params["threshold_value"] = st.slider("Percentile Cutoff (lower values split less)", min_value=5, max_value=95, value=30, step=5, key="semantic_threshold_value")
        else:
            params["threshold_value"] = st.slider("Absolute Similarity Threshold (lower splits less)", min_value=0.0, max_value=1.0, value=0.3, step=0.05, key="semantic_threshold_value")
        params["min_sentences"] = st.number_input("Min Sentences per Chunk", min_value=1, max_value=10, value=1, key="min_sentences", help="Prevents chunks smaller than this many sentences, even if similarity drops.")

    # Live summary of the active parameters, so the effect of each control is obvious at a glance
    _chip_parts = []
    for _label, _key in [
        ("Chunk Size", "chunk_size"), ("Overlap", "overlap"),
        ("Window", "window_size"), ("Step", "step_size"),
        ("Threshold", "threshold_value"), ("Min Sentences", "min_sentences"),
    ]:
        if _key in params:
            _chip_parts.append(f'<span class="param-chip"><b>{_label}:</b> {params[_key]}</span>')
    if _chip_parts:
        st.markdown(f'<div class="param-badge">{"".join(_chip_parts)}</div>', unsafe_allow_html=True)

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
            st.markdown(
                '<div class="error-hint">💡 Tip: paste your own text above, or pick one of the sample '
                'documents from the <b>Load Sample Text</b> dropdown to get started quickly.</div>',
                unsafe_allow_html=True
            )
        else:
            # Run Chunker
            txt = st.session_state.text_area_input
            st.session_state.last_processed_text = txt
            st.session_state.selected_chunk_idx = None
            try:
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
            except Exception:
                st.session_state.processed = False
                st.session_state.chunks = []
                st.error("Something went wrong while chunking your text.")
                st.markdown(
                    '<div class="error-hint">💡 Try reducing the chunk size/overlap, double-check any custom '
                    'separators, or use a shorter piece of text, then hit <b>Process</b> again.</div>',
                    unsafe_allow_html=True
                )

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
        <div class="active-summary">
            <span>🧩 <b>Technique:</b> {selected_technique}</span>
            <span>📏 <b>Target Size:</b> {c_size_str}</span>
            <span>🔗 <b>Overlap:</b> {c_overlap_str}</span>
            <span>📦 <b>Chunks:</b> {len(chunks)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Toggle Advanced Inline Visualization
        show_inline = st.checkbox("☑ Show Inline Visualization (Alternating Highlights)", value=True, help="Renders the full document with each chunk's region highlighted. Hover a highlighted region to see which chunk(s) it belongs to.")
        
        if show_inline:
            st.markdown("#### ⚡ Inline Document Highlights")
            inline_html = utils.build_inline_visualization_html(txt, chunks)
            st.markdown(inline_html, unsafe_allow_html=True)
            st.write("")

        # 3. Selected chunk detail panel
        sel_idx = st.session_state.selected_chunk_idx
        if sel_idx is not None and 0 <= sel_idx < len(chunks):
            sel_chunk = chunks[sel_idx]
            overlap_chars = utils.get_chunk_overlap_char_count(chunks, sel_idx)
            sel_tokens = sel_chunk.get("token_count")
            detail_items = [
                ("Chunk #", sel_idx + 1),
                ("Characters", len(sel_chunk["text"])),
                ("Words", len(sel_chunk["text"].split())),
                ("Start Index", sel_chunk["start_index"]),
                ("End Index", sel_chunk["end_index"]),
                ("Overlap Chars", overlap_chars),
            ]
            if sel_tokens is not None:
                detail_items.insert(3, ("Tokens", sel_tokens))

            grid_html = "".join(
                f'<div class="detail-item"><div class="val">{v}</div><div class="lbl">{l}</div></div>'
                for l, v in detail_items
            )
            dcol1, dcol2 = st.columns([10, 2])
            with dcol1:
                st.markdown(f"""
                <div class="detail-panel">
                    <b>🔍 Chunk {sel_idx + 1} details</b>
                    <div class="detail-grid">{grid_html}</div>
                </div>
                """, unsafe_allow_html=True)
            with dcol2:
                if st.button("✕ Close", key="close_detail", use_container_width=True):
                    st.session_state.selected_chunk_idx = None
                    st.rerun()

        # 4. Chunk Cards
        st.markdown("#### 📄 Chunk Cards")
        st.caption("Click **🔍** on any chunk to pin its details above, or copy its raw text.")
        for k in range(len(chunks)):
            chunk = chunks[k]
            is_selected = (st.session_state.selected_chunk_idx == k)
            bg_color = utils.get_hsl_color(k, alpha=0.10)
            border_color = utils.get_hsl_border(k, alpha=0.55)
            
            # Formatted text with bold overlaps
            bolded_html_text = utils.format_chunk_text_with_bold_overlaps(chunks, k, is_html=True)
            
            # Word count and token count if available
            words_in_chunk = len(chunk["text"].split())
            tok_count_str = f" · {chunk['token_count']} tokens" if "token_count" in chunk else ""
            selected_badge = '<span class="selected-badge">SELECTED</span>' if is_selected else ""
            card_class = "chunk-card selected" if is_selected else "chunk-card"

            card_col, action_col = st.columns([11, 1])
            with card_col:
                card_html = f"""
                <div class="{card_class}" style="background-color: {bg_color}; border-color: {border_color}; border-left-width: 5px;">
                    <div class="chunk-header">
                        <span style="color: {border_color};">🟢 Chunk {k + 1}{selected_badge}</span>
                        <span class="chunk-meta">
                            {len(chunk['text'])} chars · {words_in_chunk} words{tok_count_str} · [{chunk['start_index']}:{chunk['end_index']}]
                        </span>
                    </div>
                    <div class="chunk-body">{bolded_html_text}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
            with action_col:
                if st.button("🔍", key=f"select_chunk_{k}", help="View details for this chunk", use_container_width=True):
                    st.session_state.selected_chunk_idx = None if is_selected else k
                    st.rerun()
            
    elif st.session_state.processed and not st.session_state.chunks:
        st.markdown("""
        <div class="empty-state">
            <h1 style="font-size: 2.4rem; margin-bottom: 10px;">⚠️</h1>
            <h3>No chunks were generated</h3>
            <p>Your parameters may be too strict for this text (e.g. overlap ≥ chunk size, or thresholds that filter everything out).</p>
            <p>Try lowering overlap, increasing chunk size, or switching techniques.</p>
        </div>
        """, unsafe_allow_html=True)
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
    
    # Draw Plotly distribution chart, matching the app's dark theme
    fig = utils.generate_distribution_chart(chunk_stats["distribution_df"], theme_dark=True)
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
