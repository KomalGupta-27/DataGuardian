import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600&family=Geist:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Font Family */
    html, body, .stApp, .stMarkdown, p, label {
        font-family: 'Geist', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Target inputs, buttons, and text fields specifically without breaking icon fonts */
    .stButton > button, 
    .stDownloadButton > button, 
    .stFormSubmitButton > button,
    input, select, textarea {
        font-family: 'Geist', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    code, pre, .stCodeBlock, [data-testid="stCode"] {
        font-family: 'Geist Mono', "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important;
    }

    /* Layout & Viewport Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1400px;
    }

    /* Hide Streamlit default footer only */
    footer {visibility: hidden;}

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #0f1115 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        padding-top: 1.5rem;
    }
    
    /* Navigation Group Headers in Sidebar */
    [data-testid="stSidebarNav"] div {
        color: rgba(255, 255, 255, 0.45) !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 600 !important;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
        padding-left: 12px !important;
    }

    /* Style Navigation Links in Sidebar */
    [data-testid="stSidebarNav"] a {
        border-radius: 6px !important;
        margin: 2px 10px !important;
        padding: 6px 12px !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
        color: rgba(255, 255, 255, 0.5) !important;
        font-weight: 400 !important;
        text-decoration: none !important;
    }

    /* Hover effect */
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Active state styling (Subtle flat glass selection) */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Bento Box Card Component (Premium Dark-Tech) */
    .bento-card {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.03), 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .bento-card:hover {
        border-color: rgba(255, 255, 255, 0.15) !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
        box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 8px 30px rgba(0, 0, 0, 0.35) !important;
        transform: translateY(-2px);
    }
    
    .bento-header {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: rgba(255, 255, 255, 0.45) !important;
        margin-bottom: 10px !important;
    }
    
    .bento-value {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        line-height: 1.1 !important;
        letter-spacing: -0.03em !important;
        color: #ffffff !important;
    }

    .bento-desc {
        font-size: 0.85rem !important;
        color: rgba(255, 255, 255, 0.6) !important;
        margin-top: 8px !important;
        line-height: 1.5 !important;
    }

    /* Overwrite Streamlit Native Metrics to match Bento Design */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.03), 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(255, 255, 255, 0.15) !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
        box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 8px 25px rgba(0, 0, 0, 0.25) !important;
        transform: translateY(-1px);
    }

    div[data-testid="stMetricLabel"] > div {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: rgba(255, 255, 255, 0.45) !important;
    }

    div[data-testid="stMetricValue"] > div {
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.02em !important;
        color: #ffffff !important;
    }

    div[data-testid="stMetricDelta"] > div {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }

    /* Table & DataFrame Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.01) !important;
        overflow: hidden !important;
    }

    /* File Uploader */
    div[data-testid="stFileUploader"] {
        border: 1.5px dashed rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        background-color: rgba(255, 255, 255, 0.01) !important;
        transition: border-color 0.2s ease !important;
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Buttons Style */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.35rem !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #e2e8f0 !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #2563eb !important; /* Premium Steel Blue */
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #3b82f6 !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.3) !important;
    }

    .stButton > button:hover {
        border-color: rgba(255, 255, 255, 0.25) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        transform: translateY(-0.5px);
    }

    /* Alert and Status Banners */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
    }

    /* Headings Style */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #ffffff !important;
    }
    
    h1 {
        font-size: 2.25rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        margin-top: 1.8rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 6px;
    }

    h3 {
        font-size: 1.15rem !important;
        margin-top: 1.4rem !important;
        margin-bottom: 0.75rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Divider styling */
    hr {
        margin: 2rem 0 !important;
        border: 0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    </style>
    """, unsafe_allow_html=True)