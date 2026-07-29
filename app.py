import streamlit as st

# 1. Initialize session state for sidebar and theme (force light)
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.session_state.theme = "light"

# 2. Call set_page_config as the absolute first Streamlit call
st.set_page_config(
    page_title="RAG Chunking Visualizer",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# 3. Global CSS styles to force Light Mode everywhere (app + sidebar)
st.markdown("""
<style>
/* Force Light Mode styles globally */
.stApp {
    background-color: #FFFFFF !important;
    color: #1E1E24 !important;
}

/* Force Sidebar to be fully in Light Mode with dark text */
section[data-testid="stSidebar"] {
    background-color: #F8F9FA !important;
    border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
}

section[data-testid="stSidebar"] * {
    color: #1E1E24 !important;
}

:root {
    --text-color: #1E1E24;
    --bg-color: #FFFFFF;
    --card-bg: rgba(0, 0, 0, 0.02);
    --card-border: rgba(0, 0, 0, 0.08);
    --overlap-color: #000000;
    --stat-bg: rgba(0, 0, 0, 0.02);
    --stat-border: rgba(0, 0, 0, 0.05);
    --stat-val-color: #6E38F0;
}

p, li, label, span, .stMarkdown, .stCheckbox, .stRadio, .stSlider {
    color: #1E1E24 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #1A1A1E !important;
}

.theory-card, .chunk-card, .inline-vis-container, .stat-item {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--text-color) !important;
}

textarea, input, select {
    color: #1E1E24 !important;
    background-color: #F8F9FA !important;
    border: 1px solid rgba(0, 0, 0, 0.15) !important;
}

.overlap-bold {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# 4. Define pages
theory_page = st.Page("pages/theory.py", title="Theory", icon="📖", default=True)
playground_page = st.Page("pages/playground.py", title="Playground", icon="🎮")

# 5. Set up navigation
pg = st.navigation([theory_page, playground_page])

# 6. Run the selected page
pg.run()
