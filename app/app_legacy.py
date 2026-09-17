"""
app.py
======
DhaaraAI — Autonomous Indian Legal Intelligence Platform
Pristine, ultra-clean light mode architecture.
Strictly zero emojis, refined editorial typography, generous whitespace.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Ensure UTF-8 compatibility on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

load_dotenv(ROOT_DIR / ".env")

from bns_concordance import (
    CONCORDANCE_DB,
    lookup_by_section,
    search_crimes,
    diagnose_situation,
    get_transition_alert
)
from real_legal_fetcher import RealLegalDataService, OFFICIAL_LEGAL_HELPLINES
from embed_store import LegalEmbedStore
from rag_engine import DhaaraRAGEngine, LEGAL_DISCLAIMER

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DhaaraAI | Statutory Legal Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Pristine Light Mode Design System (Strictly Zero Emojis)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Foundation - Clean Crisp Light Mode */
    .stApp {
        background-color: #F8FAFC !important;
        background-image: none !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main Container Spacing */
    .main .block-container {
        max-width: 1200px !important;
        padding-top: 2.2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Header Bar */
    header[data-testid="stHeader"] {
        background: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    section[data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #1E293B !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    /* Top Brand Hero Block */
    .brand-hero-light {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 2rem 2.4rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02);
    }
    .brand-title-text {
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0F172A;
        margin: 0 0 0.35rem 0;
    }
    .brand-title-accent {
        color: #2563EB;
        font-weight: 800;
    }
    .brand-subtitle-text {
        font-size: 0.94rem;
        color: #475569;
        line-height: 1.55;
        margin: 0 0 1.2rem 0;
        max-width: 860px;
    }

    /* Meta Status Bar */
    .meta-status-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 1.6rem;
        align-items: center;
        padding-top: 0.9rem;
        border-top: 1px solid #F1F5F9;
        font-size: 0.78rem;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .meta-status-item {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }
    .meta-status-val {
        color: #0F172A;
        font-weight: 600;
    }
    .status-indicator-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #2563EB;
        display: inline-block;
    }

    /* Tabs Styling - Clean Light Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2.2rem !important;
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        padding: 0.85rem 0.2rem !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        color: #64748B !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1D4ED8 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #2563EB !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Section Labels */
    .section-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.9rem;
    }

    /* Buttons - Refined Modern Style */
    div.stButton > button {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.2rem !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
        min-height: 50px !important;
    }
    div.stButton > button:hover {
        background: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
    }
    div.stButton > button[kind="primary"] {
        background: #2563EB !important;
        border: 1px solid #1D4ED8 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #1D4ED8 !important;
        border-color: #1E40AF !important;
    }

    /* Chat Messages - Crisp Light Cards */
    div[data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 1.5rem 1.8rem !important;
        margin-bottom: 1.4rem !important;
        line-height: 1.7 !important;
        font-size: 0.94rem !important;
        color: #1E293B !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background: #F8FAFC !important;
        border-color: #CBD5E1 !important;
    }
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4,
    div[data-testid="stChatMessage"] strong {
        color: #0F172A !important;
    }

    /* Concordance Card - Crisp White */
    .concordance-card-light {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .concordance-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.3rem;
    }
    .concordance-sub {
        font-size: 0.86rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    .statute-dual-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .statute-column {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
    }
    .statute-col-tag {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #2563EB;
        margin-bottom: 0.3rem;
    }
    .statute-col-tag.legacy {
        color: #64748B;
    }
    .statute-col-num {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .statute-col-desc {
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.5;
    }

    /* Minimal Text Badges (Zero Emojis) */
    .badge-tag-clean {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.25rem 0.65rem;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
        display: inline-block;
        margin-right: 0.4rem;
    }
    .badge-cognizable {
        background: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .badge-nonbailable {
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }
    .badge-bailable {
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }

    /* Citation Box */
    .citation-box-light {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .citation-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .citation-section-name {
        font-size: 0.9rem;
        font-weight: 700;
        color: #0F172A;
    }
    .citation-quote {
        font-size: 0.84rem;
        color: #334155;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.6;
        background: #FFFFFF;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #E2E8F0;
        margin-top: 0.6rem;
    }

    /* Emergency Contact Card */
    .contact-card-light {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .contact-card-num {
        font-size: 1.6rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #2563EB;
        margin-bottom: 0.3rem;
    }
    .contact-card-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.4rem;
    }
    .contact-card-desc {
        font-size: 0.82rem;
        color: #64748B;
        line-height: 1.5;
    }

    /* Notice Banner */
    .statutory-banner-light {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.8rem;
        font-size: 0.88rem;
        color: #1E40AF;
        line-height: 1.55;
    }

    /* Streamlit Input Overrides */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        color: #0F172A !important;
        font-size: 0.9rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    /* Streamlit Chat Input in Light Mode */
    div[data-testid="stChatInput"] {
        padding-top: 1rem !important;
    }
    div[data-testid="stChatInput"] > div {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 0.92rem !important;
        color: #0F172A !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94A3B8 !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    div[data-testid="stExpander"] summary {
        color: #334155 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Resource Initialization
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_embed_store():
    db_path = str(ROOT_DIR / "chroma_db")
    store_obj = LegalEmbedStore(db_path=db_path)
    store_obj.seed_defaults_if_empty()
    return store_obj

store = get_embed_store()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_key" not in st.session_state:
    st.session_state.groq_key = os.getenv("GROQ_API_KEY", "").strip()

if "user_role" not in st.session_state:
    st.session_state.user_role = "general"

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_age = ""

# ---------------------------------------------------------
# Login Screen (Name & Age)
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
    <div style="max-width: 450px; margin: 4rem auto; padding: 2.5rem; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
        <h2 style="font-size: 1.8rem; font-weight: 800; color: #0F172A; text-align: center; margin-bottom: 0.5rem; letter-spacing: -0.02em;">
            DHAARA<span style="color: #2563EB;">AI</span>
        </h2>
        <p style="text-align: center; color: #64748B; font-size: 0.95rem; margin-bottom: 2rem;">
            100% Free Autonomous Statutory Legal Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            name = st.text_input("Full Name", placeholder="e.g. Rajesh Kumar")
            age = st.number_input("Age", min_value=18, max_value=120, value=25)
            submit = st.form_submit_button("Access DhaaraAI (Free)", type="primary", use_container_width=True)
            
            if submit:
                if not name.strip():
                    st.error("Please enter your name to continue.")
                else:
                    st.session_state.user_name = name.strip()
                    st.session_state.user_age = age
                    st.session_state.logged_in = True
                    st.rerun()
    st.stop()


# ---------------------------------------------------------
# Sidebar (Clean Light Mode)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="margin-bottom: 1.8rem;">
        <div style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; color: #0F172A;">
            DHAARA<span style="color: #2563EB;">AI</span>
        </div>
        <div style="font-size: 0.76rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px;">
            Statutory Intelligence Platform
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; color: #1E293B; background: #F1F5F9; padding: 0.6rem 0.8rem; border-radius: 6px;">
            👤 <b>{st.session_state.user_name}</b> (Age {st.session_state.user_age})
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Main Navigation (TheLawGPT style)
    st.markdown("<div class='section-label'>Main Menu</div>", unsafe_allow_html=True)
    nav_selection = st.radio(
        "Navigation",
        [
            "New Consultation",
            "Statute Concordance",
            "Document Review",
            "Document Generator",
            "Emergency Helplines"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #E2E8F0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # 2. Perspective
    st.markdown("<div class='section-label'>Inquiry Perspective</div>", unsafe_allow_html=True)
    role_options = {
        "general": "General Legal Inquiry",
        "victim": "Complainant / Victim (Filing Case)",
        "accused": "Accused / Notice Received (Defense)"
    }
    selected_role = st.radio(
        label="Perspective",
        options=list(role_options.keys()),
        format_func=lambda k: role_options[k],
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.user_role = selected_role

    st.markdown("<hr style='border-color: #E2E8F0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # 2. Language
    st.markdown("<div class='section-label'>Response Language</div>", unsafe_allow_html=True)
    lang_choice = st.radio(
        label="Language",
        options=["English", "Hindi (Devanagari)"],
        index=0,
        label_visibility="collapsed"
    )
    current_lang = "Hindi" if "Hindi" in lang_choice else "English"

    st.markdown("<hr style='border-color: #E2E8F0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # 3. Groq API Key
    st.markdown("<div class='section-label'>Groq API Key</div>", unsafe_allow_html=True)
    user_key = st.text_input(
        label="Groq Key",
        value=st.session_state.groq_key,
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed",
        help="Free inference key from https://console.groq.com/keys"
    )
    if user_key != st.session_state.groq_key:
        st.session_state.groq_key = user_key.strip()
        st.toast("API key updated.")

    if st.session_state.groq_key:
        st.caption("Status: Connected to Llama 3.3 70B Engine")
    else:
        st.caption("Key required for inference. Free at console.groq.com")

    st.markdown("<hr style='border-color: #E2E8F0; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # 4. Knowledge Base Summary
    st.markdown("<div class='section-label'>Statutory Knowledge Base</div>", unsafe_allow_html=True)
    stats = store.get_stats()
    st.markdown(f"""
    <div style="font-size: 0.82rem; color: #475569; line-height: 1.8;">
        <div>Indexed Chunks: <span style="color: #0F172A; font-weight: 600;">{stats['total_chunks']}</span></div>
        <div>Concordance Offenses: <span style="color: #0F172A; font-weight: 600;">{len(CONCORDANCE_DB)}</span></div>
        <div>Active Code: <span style="color: #2563EB; font-weight: 600;">BNS 2023</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("Sync IndiaCode Statutes", use_container_width=True):
        data_dir = ROOT_DIR / "data"
        store.reset_collection()
        statutes_file = str(data_dir / "comprehensive_statutes.json")
        indexed_count = store.index_statutes_json(statutes_file)
        st.toast(f"IndiaCode repository synchronized ({indexed_count} provisions).")
        st.rerun()

    st.write("")
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Clean Brand Hero (Light Mode)
# ---------------------------------------------------------
st.markdown("""
<div class="brand-hero-light">
    <h1 class="brand-title-text">DHAARA<span class="brand-title-accent">AI</span></h1>
    <p class="brand-subtitle-text">
        Autonomous Indian statutory intelligence and situational legal diagnosis platform. 
        Grounded in the Bharatiya Nyaya Sanhita (BNS 2023), BNSS 2023, BSA 2023, and landmark Supreme Court procedural directives.
    </p>
    <div class="meta-status-bar">
        <span class="meta-status-item"><span class="status-indicator-dot"></span> Active Code: <span class="meta-status-val">BNS 2023 (Post-July 1, 2024)</span></span>
        <span class="meta-status-item">Concordance: <span class="meta-status-val">IPC / CrPC Mapping</span></span>
        <span class="meta-status-item">Procedure: <span class="meta-status-val">BNSS 2023</span></span>
        <span class="meta-status-item">Inference: <span class="meta-status-val">Groq Llama 3.3 70B</span></span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# Main Content Routing
# =========================================================

if nav_selection == "New Consultation":
    # Minimal Starter Inquiries (Only shown when conversation is empty)
    if len(st.session_state.messages) == 0:
        st.markdown('<div class="section-label">Select an inquiry to evaluate:</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Online UPI or Bank Financial Scam", key="btn_upi", use_container_width=True):
                st.session_state.pending_query = "Money was fraudulently debited from my bank account through an online UPI scam. What case should be registered and what immediate steps must be taken?"
                st.session_state.user_role = "victim"
                st.rerun()
            if st.button("Notice of Appearance under Section 35 BNSS", key="btn_police_notice", use_container_width=True):
                st.session_state.pending_query = "Police has issued a notice under Section 35(3) BNSS (formerly Section 41A CrPC) directing appearance at the police station. Can police arrest immediately? What are my statutory protections?"
                st.session_state.user_role = "accused"
                st.rerun()
            if st.button("Police Refusal to Lodge First Information Report", key="btn_fir_refuse", use_container_width=True):
                st.session_state.pending_query = "The local police station is refusing to register an FIR for a cognizable offense. What is the statutory remedy under BNSS 2023 and the procedure for Zero FIR?"
                st.session_state.user_role = "victim"
                st.rerun()
        with col2:
            if st.button("Dishonour of Cheque under Section 138 NI Act", key="btn_cheque", use_container_width=True):
                st.session_state.pending_query = "A cheque issued to me was returned unpaid due to insufficient funds. What is the statutory timeline for serving legal notice under Section 138 of the Negotiable Instruments Act?"
                st.session_state.user_role = "victim"
                st.rerun()
            if st.button("Illegal Property Encroachment and Intimidation", key="btn_prop", use_container_width=True):
                st.session_state.pending_query = "Trespassers are attempting to take unlawful possession of my immovable property and issuing threats of injury. What statutory provisions under BNS apply?"
                st.session_state.user_role = "victim"
                st.rerun()
            if st.button("Rash Driving and Failure to Report Incident", key="btn_accident", use_container_width=True):
                st.session_state.pending_query = "What are the legal provisions and penalties for rash driving under Section 281 BNS and failure to report an accident under Section 106 BNS?"
                st.session_state.user_role = "general"
                st.rerun()

        st.write("")

    # Chat History
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

                if msg.get("sources"):
                    with st.expander(f"Statutory Authorities Cited ({len(msg['sources'])})", expanded=False):
                        for idx, src in enumerate(msg["sources"], 1):
                            st.markdown(f"""
                            <div class="citation-box-light">
                                <div class="citation-header-row">
                                    <span class="citation-section-name">{src.get('section', 'General')} — {src.get('section_title', '')}</span>
                                    <span style="font-size: 0.75rem; color: #64748B; font-family: monospace;">Relevance: {int(src.get('similarity_score', 0.0) * 100)}%</span>
                                </div>
                                <div style="font-size: 0.78rem; color: #64748B;">Act: {src.get('source', 'Unknown')}</div>
                                <div class="citation-quote">{src.get('text', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)

    # Chat Input
    query_from_btn = st.session_state.pop("pending_query", None)
    user_prompt = st.chat_input("Enter a statutory question or describe your legal situation...") or query_from_btn

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        engine = DhaaraRAGEngine(
            embed_store=store,
            api_key=st.session_state.groq_key
        )

        with st.chat_message("assistant"):
            with st.spinner("Analyzing statutory context and formulating grounded response..."):
                result = engine.query(
                    question=user_prompt,
                    language=current_lang,
                    user_role=st.session_state.user_role,
                    top_k=5,
                    stream=False
                )

            answer_text = result["answer"]
            sources = result["sources"]

            st.markdown(answer_text)

            if sources:
                with st.expander(f"Statutory Authorities Cited ({len(sources)})", expanded=True):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(f"""
                        <div class="citation-box-light">
                            <div class="citation-header-row">
                                <span class="citation-section-name">{src.get('section', 'General')} — {src.get('section_title', '')}</span>
                                <span style="font-size: 0.75rem; color: #64748B; font-family: monospace;">Relevance: {int(src.get('similarity_score', 0.0) * 100)}%</span>
                            </div>
                            <div style="font-size: 0.78rem; color: #64748B;">Act: {src.get('source', 'Unknown')}</div>
                            <div class="citation-quote">{src.get('text', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer_text,
                "sources": sources
            })


# =========================================================
# TAB 2: Statute Concordance
# =========================================================
elif nav_selection == "Statute Concordance":
    st.markdown("""
    <div class="statutory-banner-light">
        <b style="color: #1E3A8A;">Statutory Transition Rule:</b> 
        Effective July 1, 2024, the Bharatiya Nyaya Sanhita, 2023 (BNS) replaced the Indian Penal Code, 1860 (IPC). 
        All offenses committed on or after July 1, 2024 are registered under BNS provisions. 
        Prior offenses continue to be tried under IPC. Use the search below to cross-reference sections and classifications.
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_kw = st.text_input(
            "Search by Section number or offense name:",
            placeholder="e.g. 420, 302, 318, Cheating, Theft, Extortion...",
            label_visibility="collapsed"
        )
    with col_s2:
        cat_filter = st.selectbox(
            "Category",
            ["All Categories"] + sorted(list(set(c["category"] for c in CONCORDANCE_DB))),
            label_visibility="collapsed"
        )

    # Filter
    items = CONCORDANCE_DB
    if cat_filter != "All Categories":
        items = [c for c in items if c["category"] == cat_filter]

    if search_kw.strip():
        sec_res = lookup_by_section(search_kw)
        kw_res = search_crimes(search_kw)
        seen_ids = set()
        matched = []
        for itm in sec_res + kw_res:
            if itm["id"] not in seen_ids and (cat_filter == "All Categories" or itm["category"] == cat_filter):
                seen_ids.add(itm["id"])
                matched.append(itm)
        results = matched
    else:
        results = items

    st.caption(f"Showing {len(results)} statutory provision(s)")

    for itm in results:
        bail_badge = "badge-bailable" if "Bailable" in itm["bailable"] and "Non" not in itm["bailable"] else "badge-nonbailable"
        st.markdown(f"""
        <div class="concordance-card-light">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                <div class="concordance-title">{itm['offense_en']}</div>
                <div>
                    <span class="badge-tag-clean badge-cognizable">{itm['nature']}</span>
                    <span class="badge-tag-clean {bail_badge}">{itm['bailable']}</span>
                </div>
            </div>
            <div class="concordance-sub">{itm['offense_hi']} | Category: {itm['category']}</div>
            
            <div class="statute-dual-grid">
                <div class="statute-column">
                    <div class="statute-col-tag">Active Law (BNS 2023)</div>
                    <div class="statute-col-num">Section {itm['bns_section']}</div>
                    <div class="statute-col-desc">{itm['bns_title']}</div>
                </div>
                <div class="statute-column">
                    <div class="statute-col-tag legacy">Legacy Law (IPC 1860)</div>
                    <div class="statute-col-num">Section {itm['ipc_section']}</div>
                    <div class="statute-col-desc">{itm['ipc_title']}</div>
                </div>
            </div>

            <div style="font-size: 0.86rem; color: #1E293B; margin-bottom: 0.6rem; line-height: 1.6;">
                <b>Punishment:</b> {itm['punishment']} &nbsp;|&nbsp; <b>Triable by:</b> {itm['triable_by']}
            </div>

            <div style="font-size: 0.84rem; color: #334155; background: #F8FAFC; padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid #E2E8F0; margin-bottom: 0.8rem; line-height: 1.5;">
                <b style="color: #0F172A;">Procedure:</b> {itm['bnss_procedure']}
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.82rem; line-height: 1.5;">
                <div style="background: #F8FAFC; padding: 0.75rem; border-radius: 6px; border: 1px solid #E2E8F0;">
                    <div style="font-weight: 700; color: #1D4ED8; margin-bottom: 2px;">For Complainant:</div>
                    <div style="color: #475569;">{itm['victim_guidance']}</div>
                </div>
                <div style="background: #F8FAFC; padding: 0.75rem; border-radius: 6px; border: 1px solid #E2E8F0;">
                    <div style="font-weight: 700; color: #B45309; margin-bottom: 2px;">For Accused:</div>
                    <div style="color: #475569;">{itm['accused_guidance']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TAB 3: Legal Drafting
# =========================================================
elif nav_selection == "Document Generator":
    st.markdown("""
    <div style="margin-bottom: 1.6rem;">
        <h2 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.3rem 0;">Statutory Legal Draft Generator</h2>
        <p style="font-size: 0.88rem; color: #64748B; margin: 0;">
            Generate formal legal notices and applications with verified statutory references under BNSS Section 173 or Section 138 NI Act.
        </p>
    </div>
    """, unsafe_allow_html=True)

    draft_choice = st.selectbox(
        "Select Document Type:",
        [
            "First Information Report Application (Section 173 BNSS)",
            "Statutory Demand Notice for Dishonour of Cheque (Section 138 NI Act)",
            "Cyber Financial Fraud Reporting Application"
        ]
    )

    st.write("")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        complainant_name = st.text_input("Complainant Name:", value="Rajesh Kumar")
        complainant_contact = st.text_input("Contact Details & Address:", value="+91-9876543210, New Delhi")
        incident_date = st.date_input("Date of Incident:", value=datetime.today())
        police_station = st.text_input("Police Station / Jurisdiction:", value="Cyber Crime Police Station")

    with col_d2:
        accused_name = st.text_input("Accused / Opposite Party:", value="Person X / Organization ABC")
        loss_amount = st.text_input("Amount or Subject Matter:", value="Rs. 50,000/-")
        facts = st.text_area(
            "Summary of Facts:",
            value="The accused deceived the complainant into transferring funds on false pretenses, following which communications were ceased and obligations breached.",
            height=120
        )

    st.write("")
    if st.button("Generate Document", type="primary", use_container_width=True):
        if "Section 173 BNSS" in draft_choice:
            draft_text = f"""TO,
THE OFFICER IN CHARGE / STATION HOUSE OFFICER,
{police_station.upper()}

SUBJECT: APPLICATION UNDER SECTION 173 BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (BNSS) FOR REGISTRATION OF FIRST INFORMATION REPORT (F.I.R.)

Respected Sir/Madam,

I, {complainant_name}, residing at {complainant_contact}, do hereby submit this formal complaint as follows:

1. That on {incident_date.strftime('%d-%m-%Y')}, an offense occurred within the territorial jurisdiction of this Police Station.

2. ACCUSED DETAILS:
   Name / Identity: {accused_name}

3. STATEMENT OF FACTS:
   {facts}
   Total Financial / Material Loss: {loss_amount}

4. APPLICABLE STATUTORY PROVISIONS:
   The acts committed by the accused disclose the commission of cognizable offenses under:
   - Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (Cheating and dishonestly inducing delivery of property) [Corresponds to Section 420 IPC].
   - Section 316 of the Bharatiya Nyaya Sanhita, 2023 (Criminal Breach of Trust) [Corresponds to Section 406 IPC].
   - Relevant provisions of the Information Technology Act, 2000.

5. PRAYER:
   In view of the binding mandate of the Supreme Court in Lalita Kumari v. Govt. of U.P. and Section 173(1) BNSS, you are requested to:
   (a) Register a First Information Report (F.I.R.) immediately.
   (b) Furnish a copy of the registered F.I.R. free of cost as mandated by Section 173(2) BNSS.
   (c) Initiate an investigation in accordance with law.

Yours faithfully,

Date: {datetime.today().strftime('%d-%m-%Y')}
Place: {police_station}
Signature: __________________________
Name: {complainant_name}
Mobile: {complainant_contact}

ENCLOSURES (Admissibility under Section 63 Bharatiya Sakshya Adhiniyam):
1. Copy of Bank Statement / Transaction Slips.
2. Electronic communications / WhatsApp transcripts.
3. Identity Verification Document.
"""
        elif "Section 138" in draft_choice:
            draft_text = f"""REGISTERED POST WITH ACKNOWLEDGEMENT DUE / STATUTORY NOTICE

Date: {datetime.today().strftime('%d-%m-%Y')}

TO,
{accused_name}
[Full Address of the Drawer]

SUBJECT: LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 FOR DISHONOUR OF CHEQUE FOR AMOUNT {loss_amount}.

Sir / Madam,

Under instructions from my client, {complainant_name} (Address: {complainant_contact}), I hereby serve upon you this Statutory Legal Demand Notice:

1. That in discharge of a legally enforceable debt/liability, you issued Cheque bearing No. [Insert Cheque Number] drawn on [Bank Name] for an amount of {loss_amount} in favour of my client.

2. That the said cheque was presented for clearance within its validity period. However, the said cheque was returned unpaid by the bank vide Return Memo dated {incident_date.strftime('%d-%m-%Y')} with the remarks: "FUNDS INSUFFICIENT / EXCEEDS ARRANGEMENT".

3. FACTUAL SUMMARY:
   {facts}

4. That by dishonouring the said cheque, you have committed an offense punishable under Section 138 of the Negotiable Instruments Act, 1881.

5. DEMAND:
   I hereby demand that you pay the full amount of {loss_amount} to my client within FIFTEEN (15) DAYS of receipt of this notice.

6. Failure to comply with this notice within 15 days shall leave my client with no option but to initiate criminal proceedings against you under Section 138 of the Negotiable Instruments Act and Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 before the competent Court of Judicial Magistrate.

Advocate for Complainant
Signature: ______________________
"""
        else:
            draft_text = f"""NATIONAL CYBER CRIME REPORTING PORTAL (cybercrime.gov.in / 1930)
OFFICIAL INCIDENT DOSSIER

Category: Cyber Financial Fraud / Identity Deception
Date of Incident: {incident_date.strftime('%d-%m-%Y')}
Complainant: {complainant_name} | {complainant_contact}
Suspect Details: {accused_name}
Total Disputed Amount: {loss_amount}

SUMMARY OF INCIDENT:
{facts}

EVIDENCE RECORD UNDER SECTION 63 BHARATIYA SAKSHYA ADHINIYAM (BSA 2023):
- Transaction Reference Numbers (UTR)
- Bank Account Debit Record
- Electronic Communication Logs and IP Records
- Device Authenticity Certificate under Section 63 BSA

RELIEF SOUGHT:
Immediate freezing of beneficiary accounts through the 1930 Citizen Financial Cyber Fraud Reporting System and registration of case under Section 318(4) BNS 2023 read with Sections 66C and 66D of the Information Technology Act, 2000.
"""

        st.markdown('<div class="section-label" style="margin-top: 1.5rem;">Generated Document:</div>', unsafe_allow_html=True)
        st.code(draft_text, language="text")
        st.download_button(
            label="Download Document (.txt)",
            data=draft_text,
            file_name=f"Legal_Notice_{complainant_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# TAB 4: Document Review (Placeholder)
# =========================================================
elif nav_selection == "Document Review":
    st.markdown("""
    <div style="margin-bottom: 1.6rem;">
        <h2 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.3rem 0;">Legal Document Review</h2>
        <p style="font-size: 0.88rem; color: #64748B; margin: 0;">
            Upload your contracts, notices, or FIR copies for AI-powered risk analysis and statutory vetting.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Document Upload and OCR processing modules are currently offline in this environment. Please paste the text in 'New Consultation' for review.")

# =========================================================
# TAB 5: Emergency Contacts & Citizen Rights
# =========================================================
elif nav_selection == "Emergency Helplines":
    st.markdown("""
    <div style="margin-bottom: 1.8rem;">
        <h2 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.3rem 0;">Official Government Helplines</h2>
        <p style="font-size: 0.88rem; color: #64748B; margin: 0;">
            Central government emergency response numbers and legal aid portals under Article 39A of the Constitution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)
    helplines = RealLegalDataService.get_helplines()

    for idx, h in enumerate(helplines):
        target = col_c1 if idx % 3 == 0 else (col_c2 if idx % 3 == 1 else col_c3)
        with target:
            st.markdown(f"""
            <div class="contact-card-light">
                <div class="contact-card-num">{h['number']}</div>
                <div class="contact-card-title">{h['service']}</div>
                <div style="font-size: 0.74rem; font-weight: 700; color: #2563EB; text-transform: uppercase; margin-bottom: 0.5rem;">{h['type']}</div>
                <div class="contact-card-desc">{h['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Citizen Safeguards under BNSS 2023</div>', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("""
        <div class="concordance-card-light" style="margin-bottom: 1rem;">
            <div style="font-weight: 700; color: #0F172A; font-size: 0.95rem; margin-bottom: 0.5rem;">Arrest vs Section 35(3) Notice Safeguard</div>
            <ul style="font-size: 0.85rem; color: #475569; line-height: 1.65; padding-left: 1.2rem; margin: 0;">
                <li>For offenses punishable with imprisonment up to 7 years, routine police arrest is prohibited by statute.</li>
                <li>The Investigating Officer must issue a formal Notice of Appearance under Section 35(3) BNSS (formerly Section 41A CrPC).</li>
                <li>As long as the citizen complies with the notice and appears for questioning, arrest is barred unless specific reasons of flight risk or witness tampering are recorded in writing and submitted to the Magistrate.</li>
            </ul>
        </div>
        <div class="concordance-card-light">
            <div style="font-weight: 700; color: #0F172A; font-size: 0.95rem; margin-bottom: 0.5rem;">Remedy if Police Refuses to Register FIR</div>
            <ul style="font-size: 0.85rem; color: #475569; line-height: 1.65; padding-left: 1.2rem; margin: 0;">
                <li>Under Section 173(1) BNSS and the Supreme Court judgment in Lalita Kumari, registration of FIR is mandatory for all cognizable offenses.</li>
                <li>Zero FIR: A citizen can lodge a complaint at any police station regardless of territorial jurisdiction.</li>
                <li>Escalation: If the Station House Officer refuses, a written complaint may be sent to the Superintendent of Police under Section 173(4) BNSS.</li>
                <li>Magistrate Application: An application accompanied by an affidavit can be made before the Judicial Magistrate under Section 175(3) BNSS.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("""
        <div class="concordance-card-light" style="margin-bottom: 1rem;">
            <div style="font-weight: 700; color: #0F172A; font-size: 0.95rem; margin-bottom: 0.5rem;">Rights of an Arrested Person</div>
            <ul style="font-size: 0.85rem; color: #475569; line-height: 1.65; padding-left: 1.2rem; margin: 0;">
                <li>Right to meet an advocate of choice during interrogation under Section 47 BNSS.</li>
                <li>Right to inform a relative or friend immediately upon arrest under Section 48 BNSS.</li>
                <li>Mandatory medical examination by a government medical officer under Section 53 BNSS.</li>
                <li>Mandatory production before the nearest Judicial Magistrate within 24 hours of arrest without exception.</li>
            </ul>
        </div>
        <div class="concordance-card-light">
            <div style="font-weight: 700; color: #0F172A; font-size: 0.95rem; margin-bottom: 0.5rem;">Free Legal Defense (NALSA)</div>
            <ul style="font-size: 0.85rem; color: #475569; line-height: 1.65; padding-left: 1.2rem; margin: 0;">
                <li>All women, children, persons in police custody, and indigent citizens are legally entitled to 100% free legal representation by government-appointed advocates.</li>
                <li>Call toll-free helpline 1516 or approach the District Legal Services Authority (DLSA) in your district court complex.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
