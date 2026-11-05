import streamlit as st

# ---------------------------------------------------------------------------
# StudyMind design system
# Neutral slate surfaces, one indigo accent, Inter typography, flat cards with
# hairline borders. Tokens live in :root so every widget and component shares
# the same palette.
# ---------------------------------------------------------------------------

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0B0E14;
    --surface: #11151D;
    --surface-2: #161B26;
    --surface-3: #1C2230;
    --border: #232A38;
    --border-strong: #303949;
    --text: #E6E9EF;
    --text-muted: #8B93A5;
    --text-faint: #5F687B;
    --accent: #6366F1;
    --accent-hover: #7578F5;
    --accent-soft: rgba(99, 102, 241, 0.14);
    --accent-border: rgba(99, 102, 241, 0.38);
    --success: #34D399;
    --warning: #FBBF24;
    --danger: #FB7185;
    --radius: 12px;
    --radius-sm: 8px;
    --shadow: 0 1px 2px rgba(0, 0, 0, 0.35), 0 8px 24px -12px rgba(0, 0, 0, 0.5);
}

/* ---------- Base ---------- */
html, body, .stApp, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
}
.stApp { background: var(--bg) !important; color: var(--text); }

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.02em;
    font-weight: 650 !important;
}
h3 { font-size: 1.1rem !important; }
h4 { font-size: 1rem !important; }
p, li { color: var(--text); line-height: 1.65; }
a { color: var(--accent-hover) !important; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.6rem 0 !important; }
code {
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--surface-3) !important;
    color: #C7D2FE !important;
    border-radius: 6px; padding: 0.12em 0.4em; font-size: 0.86em;
}
[data-testid="stCaptionContainer"], .stCaption, small { color: var(--text-muted) !important; }

header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stDecoration"] { visibility: hidden; display: none; }

.block-container {
    padding-top: 2.4rem !important;
    padding-bottom: 4rem !important;
    max-width: 1240px !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0.4rem; }
section[data-testid="stSidebar"] hr { margin: 1rem 0 !important; }

/* Navigation: radio restyled as a vertical menu */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label { display: none !important; }
section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child { display: none !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    width: 100%;
    padding: 8px 12px !important;
    margin: 0 !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label p,
section[data-testid="stSidebar"] div[data-testid="stRadio"] label span {
    color: var(--text-muted) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover { background: var(--surface-2) !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p,
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover span { color: var(--text) !important; }
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--accent-soft) !important;
    border-color: var(--accent-border) !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p,
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ---------- Widgets: labels & inputs ---------- */
div[data-testid="stWidgetLabel"] p, .stWidgetLabel p, label p {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input,
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-size: 0.93rem !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stTextInput input:hover, .stTextArea textarea:hover, div[data-baseweb="select"] > div:hover {
    border-color: var(--border-strong) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
input::placeholder, textarea::placeholder { color: var(--text-faint) !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: var(--text) !important; }

div[data-baseweb="popover"] > div, ul[role="listbox"], div[data-baseweb="menu"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.55) !important;
}
li[role="option"] { background: transparent !important; color: var(--text) !important; font-size: 0.9rem !important; }
li[role="option"]:hover, li[role="option"][aria-selected="true"] { background: var(--accent-soft) !important; }

/* Radios (main area), toggles, sliders */
.stRadio [role="radiogroup"] label p { color: var(--text) !important; font-weight: 500 !important; font-size: 0.9rem !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--accent) !important; box-shadow: 0 0 0 4px var(--accent-soft) !important; }
div[data-testid="stThumbValue"], div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] { color: var(--text-muted) !important; font-size: 0.78rem !important; }
.stCheckbox label p, .stToggle label p { color: var(--text) !important; font-weight: 500 !important; font-size: 0.92rem !important; }

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border-strong) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--accent) !important; background: var(--accent-soft) !important; }

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button,
button[data-testid^="stBaseButton-"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.1rem !important;
    min-height: 2.5rem;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.1s ease !important;
}
/* Secondary (default) */
.stButton > button[kind="secondary"], .stDownloadButton > button, button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-secondaryFormSubmit"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-strong) !important;
    color: var(--text) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background: var(--surface-3) !important;
    border-color: var(--accent-border) !important;
    color: #FFFFFF !important;
}
/* Primary */
.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"], .stFormSubmitButton > button[kind="primary"] {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    color: #FFFFFF !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
}
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
}
.stButton > button p, .stFormSubmitButton > button p, .stDownloadButton > button p {
    color: inherit !important; font-weight: 600 !important; font-size: 0.9rem !important; margin: 0;
}
.stButton > button:active { transform: translateY(1px); }
.stButton > button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.stButton > button:disabled { opacity: 0.45; }

/* ---------- Containers, expanders, tabs ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) { border-radius: var(--radius); }
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
}
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}
div[data-testid="stExpander"] summary { padding: 0.7rem 1rem; }
div[data-testid="stExpander"] summary p { color: var(--text) !important; font-weight: 600 !important; font-size: 0.9rem !important; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--border); background: transparent; padding: 0; }
.stTabs [data-baseweb="tab"] {
    background: transparent !important; padding: 10px 16px; border-radius: 0; height: auto;
}
.stTabs [data-baseweb="tab"] p { color: var(--text-muted) !important; font-weight: 600 !important; font-size: 0.9rem !important; }
.stTabs [data-baseweb="tab"]:hover p { color: var(--text) !important; }
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--accent) !important; height: 2px !important; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Alerts */
div[data-testid="stAlert"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}
div[data-testid="stAlert"] p { color: var(--text) !important; font-size: 0.92rem !important; }

/* Native metrics, progress, tables */
div[data-testid="stMetric"] {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 14px 16px;
}
div[data-testid="stMetricLabel"] p { color: var(--text-muted) !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
div[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700 !important; }
.stProgress > div > div > div > div { background: var(--accent) !important; }
.stProgress > div > div > div { background: var(--surface-3) !important; }
div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
div[data-testid="stCodeBlock"], pre { border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; background: var(--surface) !important; }
div[data-testid="stSpinner"] p { color: var(--text-muted) !important; }

/* ---------- Chat ---------- */
div[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
    gap: 0.9rem;
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: var(--surface-2) !important; }
div[data-testid="stChatMessage"] p { font-size: 0.94rem; }
div[data-testid="stChatMessageAvatarUser"], div[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--accent-soft) !important; color: #C7D2FE !important; border: 1px solid var(--accent-border);
}
div[data-testid="stChatInput"] {
    background: var(--surface-2) !important; border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius) !important;
}
div[data-testid="stChatInput"]:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft); }
div[data-testid="stChatInput"] textarea { background: transparent !important; border: none !important; box-shadow: none !important; }
div[data-testid="stBottom"] > div { background: var(--bg) !important; }

/* ---------- Custom components ---------- */
.sm-brand { display: flex; align-items: center; gap: 11px; padding: 14px 6px 18px; }
.sm-brand-mark {
    width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.7);
}
.sm-brand-mark svg { width: 18px; height: 18px; stroke: #fff; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.sm-brand-name { font-size: 1.05rem; font-weight: 700; color: var(--text); letter-spacing: -0.02em; line-height: 1.1; }
.sm-brand-tag { font-size: 0.7rem; color: var(--text-faint); font-weight: 500; letter-spacing: 0.02em; margin-top: 2px; }

.sm-user {
    display: flex; align-items: center; gap: 11px; padding: 11px 12px;
    background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius);
}
.sm-avatar {
    width: 34px; height: 34px; flex: none; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    background: var(--accent-soft); border: 1px solid var(--accent-border); color: #C7D2FE; font-weight: 700; font-size: 0.85rem;
}
.sm-user-name { font-size: 0.86rem; font-weight: 600; color: var(--text); line-height: 1.25; }
.sm-user-meta { font-size: 0.72rem; color: var(--text-muted); line-height: 1.35; }

.sm-page-header { margin-bottom: 1.6rem; padding-bottom: 1.2rem; border-bottom: 1px solid var(--border); }
.sm-eyebrow {
    display: inline-block; font-size: 0.7rem; font-weight: 700; color: var(--accent-hover);
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;
}
.sm-page-title { font-size: 1.85rem; font-weight: 750; color: var(--text); letter-spacing: -0.03em; line-height: 1.2; margin: 0; }
.sm-page-sub { font-size: 0.97rem; color: var(--text-muted); margin: 8px 0 0; max-width: 760px; line-height: 1.55; }

.sm-section-title { font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.09em; margin: 0.4rem 0 0.9rem; }

.sm-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 20px 22px; margin-bottom: 16px; box-shadow: var(--shadow);
}
.sm-card p:last-child, .sm-card-accent p:last-child { margin-bottom: 0; }
.sm-card-gradient, .sm-card-accent {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.13) 0%, rgba(99, 102, 241, 0.04) 100%), var(--surface);
    border: 1px solid var(--accent-border); border-radius: var(--radius);
    padding: 20px 22px; margin-bottom: 16px;
}

.sm-stat { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px 20px; box-shadow: var(--shadow); height: 100%; }
.sm-stat-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.sm-stat-label { font-size: 0.74rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.07em; }
.sm-stat-value { font-size: 1.9rem; font-weight: 700; color: var(--text); letter-spacing: -0.03em; line-height: 1.1; }
.sm-stat-sub { font-size: 0.78rem; color: var(--text-faint); margin-top: 6px; }
.sm-icon {
    width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center;
    background: var(--accent-soft); border: 1px solid var(--accent-border);
}
.sm-icon svg { width: 17px; height: 17px; stroke: #A5B4FC; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

.sm-feature-title { font-size: 0.98rem; font-weight: 650; color: var(--text); margin: 12px 0 4px; letter-spacing: -0.01em; }
.sm-feature-desc { font-size: 0.84rem; color: var(--text-muted); line-height: 1.5; min-height: 2.5em; margin: 0 0 6px; }

.sm-chip {
    display: inline-flex; align-items: center; gap: 8px; background: var(--surface-2);
    border: 1px solid var(--border-strong); border-radius: 999px; padding: 5px 6px 5px 12px;
    font-size: 0.8rem; font-weight: 500; color: var(--text); margin: 3px 6px 3px 0;
}
.sm-chip-page { color: var(--text-muted); }
.sm-chip-score { background: var(--accent-soft); color: #C7D2FE; border-radius: 999px; padding: 2px 9px; font-weight: 600; font-size: 0.74rem; }

.sm-progress { height: 6px; border-radius: 999px; background: var(--surface-3); overflow: hidden; margin-top: 14px; }
.sm-progress > div { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #6366F1, #8B5CF6); }

.sm-badge {
    display: inline-flex; align-items: center; gap: 6px; font-size: 0.72rem; font-weight: 600; color: var(--text-muted);
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 999px; padding: 3px 10px;
}

.sm-flashcard {
    min-height: 260px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
    padding: 36px 44px; border-radius: 16px; background: var(--surface); border: 1px solid var(--border-strong);
    box-shadow: var(--shadow); margin: 6px 0 18px;
}
.sm-flashcard.is-answer { background: linear-gradient(135deg, rgba(99, 102, 241, 0.14), rgba(99, 102, 241, 0.04)), var(--surface); border-color: var(--accent-border); }
.sm-flashcard-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent-hover); margin-bottom: 14px; }
.sm-flashcard-text { font-size: 1.3rem; font-weight: 600; color: var(--text); line-height: 1.5; letter-spacing: -0.01em; margin: 0; }
.sm-flashcard.is-answer .sm-flashcard-text { font-size: 1.1rem; font-weight: 500; }
.sm-flashcard-hint { margin-top: 20px; font-size: 0.78rem; color: var(--text-faint); }

/* Auth screen */
.sm-auth-hero { padding: 8px 8px 0 0; }
.sm-auth-hero h1 { font-size: 2.5rem !important; line-height: 1.12; font-weight: 750 !important; letter-spacing: -0.035em; margin: 18px 0 14px; }
.sm-auth-hero h1 span { background: linear-gradient(90deg, #A5B4FC, #C4B5FD); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.sm-auth-hero p.lead { color: var(--text-muted); font-size: 1.02rem; max-width: 460px; }
.sm-auth-points { margin-top: 26px; display: grid; gap: 14px; }
.sm-auth-point { display: flex; gap: 12px; align-items: flex-start; }
.sm-auth-point .sm-icon { flex: none; }
.sm-auth-point b { display: block; color: var(--text); font-size: 0.92rem; font-weight: 600; }
.sm-auth-point span { color: var(--text-muted); font-size: 0.84rem; line-height: 1.45; }

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 8px; border: 2px solid var(--bg); }
::-webkit-scrollbar-thumb:hover { background: var(--text-faint); }
</style>
"""


def inject_custom_css():
    """Injects the StudyMind design system (tokens, widget overrides, components)."""
    st.markdown(_CSS, unsafe_allow_html=True)
