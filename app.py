import streamlit as st
import utils

# 1. Initialize session state for sidebar and theme (dark developer-tool theme)
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.session_state.theme = "dark"

# 2. Call set_page_config as the absolute first Streamlit call
st.set_page_config(
    page_title="RAG Chunking Visualizer",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# 3. Global theme: a single, consistent dark developer-tool aesthetic
# applied app-wide (see utils/theme.py). Individual pages layer on
# page-specific component styles on top of these shared tokens.
st.markdown(utils.base_theme_css(), unsafe_allow_html=True)

# 4. Define pages
theory_page = st.Page("pages/theory.py", title="Theory", icon="📖", default=True)
playground_page = st.Page("pages/playground.py", title="Playground", icon="🎮")

# 5. Set up navigation
pg = st.navigation([theory_page, playground_page])

# 6. Run the selected page
pg.run()
