"""
main.py
=======
Main entry point for DhaaraAI Application.
Wires up styles and routes to views based on state.
"""
import sys
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Ensure UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))
load_dotenv(ROOT_DIR / ".env")

# Must be called first
st.set_page_config(
    page_title="DhaaraAI | Autonomous Legal Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize styles
from styles import inject_global_styles
inject_global_styles()

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_age = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_role" not in st.session_state:
    st.session_state.user_role = "general"
if "current_view" not in st.session_state:
    st.session_state.current_view = "New Consultation"

# RAG Engine Init
from embed_store import LegalEmbedStore
from rag_engine import DhaaraRAGEngine

@st.cache_resource(show_spinner=False)
def get_embed_store():
    db_path = str(ROOT_DIR / "chroma_db")
    store_obj = LegalEmbedStore(db_path=db_path)
    store_obj.seed_defaults_if_empty()
    return store_obj

store = get_embed_store()
api_key = os.getenv("GROQ_API_KEY", "").strip()
engine = DhaaraRAGEngine(embed_store=store, api_key=api_key) if api_key else None

# Router
if not st.session_state.logged_in:
    from views.landing import render_landing
    render_landing()
else:
    from views.sidebar import render_sidebar
    render_sidebar()
    
    # Router based on selection
    if st.session_state.current_view == "Consultation":
        from views.consultation import render_consultation_view
        render_consultation_view(engine=engine)
    elif st.session_state.current_view == "Document Generator":
        from views.generator import render_generator
        render_generator()
    elif st.session_state.current_view == "Statute Concordance":
        from views.concordance import render_concordance
        render_concordance()
    elif st.session_state.current_view == "Helplines":
        from views.helplines import render_helplines
        render_helplines()
