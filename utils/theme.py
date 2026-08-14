"""
Shared visual theme for the RAG Chunking Visualizer.

Centralizes the color system, typography and base component styles so that
app.py, pages/theory.py and pages/playground.py all render a single,
consistent dark developer-tool aesthetic instead of each page rolling its
own CSS.
"""

# ---------------------------------------------------------------------------
# Core color tokens - a small, deliberately restrained palette.
# ---------------------------------------------------------------------------
COLORS = {
    "bg_primary": "#0B0F17",       # app background - deep charcoal/navy
    "bg_secondary": "#11172400",   # unused placeholder (kept for clarity)
    "bg_panel": "#111827",         # cards / panels
    "bg_panel_alt": "#161F2E",     # nested inputs, subtler surfaces
    "bg_hover": "#1B2536",         # hover surface
    "border": "rgba(148, 163, 184, 0.14)",
    "border_strong": "rgba(148, 163, 184, 0.28)",
    "text_primary": "#E7ECF3",     # headings / body
    "text_secondary": "#9AA7B8",   # metadata / secondary text
    "text_tertiary": "#6B7688",    # placeholders / faint labels
    "accent_primary": "#22D3EE",   # cyan - primary accent
    "accent_secondary": "#A78BFA",  # violet - secondary accent
    "accent_primary_glow": "rgba(34, 211, 238, 0.16)",
    "accent_secondary_glow": "rgba(167, 139, 250, 0.16)",
    "success": "#34D399",
    "error": "#F87171",
    "warning": "#FBBF24",
}

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;700&"
    "family=JetBrains+Mono:wght@400;500&display=swap');"
)


def base_theme_css() -> str:
    """Global theme applied once, at the top of app.py."""
    c = COLORS
    return f"""
    <style>
    {FONT_IMPORT}

    :root {{
        --bg-primary: {c['bg_primary']};
        --bg-panel: {c['bg_panel']};
        --bg-panel-alt: {c['bg_panel_alt']};
        --bg-hover: {c['bg_hover']};
        --border-color: {c['border']};
        --border-strong: {c['border_strong']};
        --text-primary: {c['text_primary']};
        --text-secondary: {c['text_secondary']};
        --text-tertiary: {c['text_tertiary']};
        --accent-primary: {c['accent_primary']};
        --accent-secondary: {c['accent_secondary']};
        --accent-primary-glow: {c['accent_primary_glow']};
        --accent-secondary-glow: {c['accent_secondary_glow']};
        --success: {c['success']};
        --error: {c['error']};
        --warning: {c['warning']};
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }}

    /* ---------- App shell ---------- */
    .stApp {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}

    .main .block-container {{
        font-family: 'Inter', sans-serif;
        padding-top: 2rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: var(--bg-panel) !important;
        border-right: 1px solid var(--border-color) !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: var(--text-primary) !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stPageLink"] {{
        border-radius: var(--radius-sm);
    }}

    header[data-testid="stHeader"] {{
        background-color: var(--bg-primary) !important;
    }}

    /* ---------- Typography ---------- */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        color: var(--text-primary) !important;
        letter-spacing: -0.3px;
    }}
    p, li, label, span, .stMarkdown, .stCheckbox, .stRadio, .stCaption {{
        color: var(--text-primary);
    }}
    .stCaption, small, [data-testid="stCaptionContainer"] {{
        color: var(--text-secondary) !important;
    }}

    .gradient-text, .gradient-title {{
        background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}

    /* ---------- Inputs & controls ---------- */
    textarea, input, select {{
        color: var(--text-primary) !important;
        background-color: var(--bg-panel-alt) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
    }}
    textarea::placeholder, input::placeholder {{
        color: var(--text-tertiary) !important;
        opacity: 1 !important;
    }}
    textarea:focus, input:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px var(--accent-primary-glow) !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: var(--bg-panel-alt) !important;
        border-color: var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }}
    div[data-baseweb="select"] * {{
        color: var(--text-primary) !important;
    }}
    ul[data-testid="stSelectboxVirtualDropdown"] {{
        background-color: var(--bg-panel-alt) !important;
    }}
    li[role="option"] {{
        color: var(--text-primary) !important;
    }}
    li[role="option"]:hover, li[aria-selected="true"] {{
        background-color: var(--bg-hover) !important;
    }}

    /* Slider */
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
        background: var(--border-strong) !important;
    }}
    div[data-testid="stSlider"] [role="slider"] {{
        background-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 4px var(--accent-primary-glow) !important;
    }}
    div[data-testid="stTickBar"] {{ display: none; }}
    div[data-testid="stSliderTickBarMin"], div[data-testid="stSliderTickBarMax"] {{
        color: var(--text-tertiary) !important;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: var(--bg-panel-alt);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        font-weight: 500;
        transition: all 0.15s ease;
    }}
    .stButton > button:hover {{
        border-color: var(--accent-primary);
        color: var(--accent-primary);
        background-color: var(--bg-hover);
    }}
    .stButton > button:active {{
        transform: scale(0.98);
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
        border: none;
        color: #0B0F17;
        font-weight: 700;
    }}
    .stButton > button[kind="primary"]:hover {{
        filter: brightness(1.08);
        color: #0B0F17;
        box-shadow: 0 0 20px var(--accent-primary-glow);
    }}

    /* Radio / checkbox */
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {{
        color: var(--text-primary) !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        color: var(--text-secondary) !important;
        font-weight: 500;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--accent-primary) !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: var(--accent-primary) !important;
    }}
    div[data-baseweb="tab-border"] {{
        background-color: var(--border-color) !important;
    }}

    /* Alerts */
    div[data-testid="stAlertContainer"] {{
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-color) !important;
    }}

    /* Misc */
    hr {{
        border-color: var(--border-color) !important;
    }}
    code {{
        color: var(--accent-primary) !important;
        background-color: var(--bg-panel-alt) !important;
    }}

    /* Scrollbars */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg-panel); }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--accent-primary); }}

    /* Responsive tweaks */
    @media (max-width: 768px) {{
        .main .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
        h1 {{ font-size: 1.6rem !important; }}
    }}
    </style>
    """
