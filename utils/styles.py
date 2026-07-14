import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Layout */
    .block-container{
        padding-top:1.2rem;
        padding-bottom:2rem;
        padding-left:2rem;
        padding-right:2rem;
    }

    html, body, [class*="css"]{
        font-family: "Inter","Segoe UI",sans-serif;
    }

    /* Don't force text colors - let Streamlit theme handle them */

    h1{
        font-weight:700;
    }

    h2,h3{
        font-weight:600;
    }

    /* Metric Cards */

    div[data-testid="stMetric"]{
        border:1px solid rgba(128,128,128,.25);
        border-radius:12px;
        padding:15px;
        background:transparent;
    }

    /* DataFrames */

    div[data-testid="stDataFrame"]{
        border-radius:12px;
        overflow:hidden;
    }

    /* File uploader */

    div[data-testid="stFileUploader"]{
        border-radius:12px;
    }

    /* Buttons */

    .stButton>button{
        border-radius:10px;
        font-weight:600;
        padding:0.55rem 1rem;
    }

    /* Sidebar */

    section[data-testid="stSidebar"]{
        border-right:1px solid rgba(128,128,128,.15);
    }

    /* Tabs */

    button[role="tab"]{
        font-weight:600;
    }

    </style>
    """, unsafe_allow_html=True)