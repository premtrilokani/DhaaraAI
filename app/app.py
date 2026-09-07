"""
app.py
======
DhaaraAI — Autonomous Legal Intelligence & Statutory RAG Platform
Elite Dark-Mode Interface with Glassmorphism, Micro-Animations, and Precise Citations.
"""

import sys
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Ensure Unicode / UTF-8 compatibility on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add src to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

load_dotenv(ROOT_DIR / ".env")

from embed_store import LegalEmbedStore
from rag_engine import DhaaraRAGEngine, DISCLAIMER_EN, DISCLAIMER_HI
from pdf_loader import load_all_pdfs
from chunker import process_pages_into_chunks


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DhaaraAI | Legal Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Elite Dark-Mode Design System & Glassmorphism CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Dark Theme */
    .stApp {
        background-color: #07090E !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(30, 58, 138, 0.22) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(88, 28, 135, 0.18) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.5) 0px, transparent 60%) !important;
        color: #F1F5F9 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Hide standard Streamlit header decoration */
    header[data-testid="stHeader"] {
        background: rgba(7, 9, 14, 0.7) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }
    section[data-testid="stSidebar"] div.block-container {
        padding-top: 1.5rem !important;
    }

    /* Hero Branding Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 2.2rem 2.6rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
    }
    .brand-row {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin-bottom: 0.6rem;
    }
    .brand-logo-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        color: #FFFFFF;
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
    }
    .brand-title span.accent {
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-tagline {
        color: #94A3B8;
        font-size: 0.98rem;
        font-weight: 400;
        margin-bottom: 1.4rem;
        max-width: 820px;
        line-height: 1.5;
    }

    /* Live System Status Strip */
    .status-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        align-items: center;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 0.35rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: #CBD5E1;
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
        display: inline-block;
        animation: pulseAnimation 2s infinite;
    }
    @keyframes pulseAnimation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Modern Prompt Selector Cards */
    .prompt-section-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 0.9rem;
    }

    /* Custom Streamlit Buttons in Dark Mode */
    div.stButton > button {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.1rem !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
    }
    div.stButton > button:hover {
        background: rgba(30, 41, 59, 0.9) !important;
        border-color: rgba(99, 102, 241, 0.6) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.3) !important;
    }

    /* Primary Action Button (Gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #6D28D9 100%) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.55) !important;
    }

    /* Stat Cards in Sidebar */
    .stat-card-dark {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.9rem;
        text-align: center;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    .stat-num-glow {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .stat-lbl {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* Chat Messages Styling */
    div[data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 1.3rem 1.6rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        background: rgba(30, 41, 59, 0.4) !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
    }

    /* Citation Card Design */
    .citation-container {
        background: rgba(11, 15, 25, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #6366F1;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .citation-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }
    .citation-sec-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #F8FAFC;
    }
    .match-badge {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #A5B4FC;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
    }
    .citation-meta-row {
        font-size: 0.78rem;
        color: #64748B;
        margin-bottom: 0.65rem;
        display: flex;
        gap: 1.2rem;
    }
    .statutory-quote {
        font-size: 0.85rem;
        line-height: 1.55;
        color: #CBD5E1;
        background: rgba(7, 9, 14, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 6px;
        padding: 0.75rem 0.95rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Disclaimer Callout */
    .disclaimer-card {
        background: rgba(245, 158, 11, 0.06);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-left: 3px solid #F59E0B;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #FCD34D;
        line-height: 1.45;
        margin-top: 1rem;
    }

    /* Chat Input Styling */
    div[data-testid="stChatInput"] {
        background: transparent !important;
    }
    div[data-testid="stChatInput"] > div {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #F8FAFC !important;
        font-size: 0.92rem !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748B !important;
    }

    /* Streamlit Expander styling */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] summary {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Resource Initialization (Cached)
# ---------------------------------------------------------
@st.cache_resource(show_spinner="Connecting to persistent ChromaDB vector store...")
def get_embed_store():
    db_path = str(ROOT_DIR / "chroma_db")
    return LegalEmbedStore(db_path=db_path)


store = get_embed_store()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_key" not in st.session_state:
    st.session_state.groq_key = os.getenv("GROQ_API_KEY", "").strip()


# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.4rem 0 1.2rem 0;">
        <div style="font-size: 1.45rem; font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF;">
            DHAARA<span style="color: #60A5FA;">.AI</span>
        </div>
        <div style="font-size: 0.78rem; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
            Statutory Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Language Toggle
    st.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>Response Language</div>", unsafe_allow_html=True)
    lang_choice = st.radio(
        label="Response Language",
        options=["English", "Hindi (देवनागरी)"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    current_lang = "Hindi" if "Hindi" in lang_choice else "English"

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # 2. Groq API Key Setup
    st.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>Groq API Inference Key</div>", unsafe_allow_html=True)
    user_key = st.text_input(
        label="Groq Key",
        value=st.session_state.groq_key,
        type="password",
        placeholder="gsk_...",
        help="Free API key from https://console.groq.com/keys",
        label_visibility="collapsed"
    )

    if user_key != st.session_state.groq_key:
        st.session_state.groq_key = user_key.strip()
        st.toast("API key updated for current session.")

    if st.session_state.groq_key:
        st.markdown("<div style='font-size: 0.76rem; color: #10B981; font-weight: 500; margin-top: 4px;'>● Connected to Llama 3.3 70B Engine</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size: 0.76rem; color: #F59E0B; margin-top: 4px;'>Key required for inference. Free tier at console.groq.com</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # 3. Knowledge Base Status & Indexing
    st.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Statutory Knowledge Base</div>", unsafe_allow_html=True)
    stats = store.get_stats()

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f"""
        <div class="stat-card-dark">
            <div class="stat-num-glow">{stats['total_chunks']}</div>
            <div class="stat-lbl">Indexed Chunks</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        data_dir = ROOT_DIR / "data"
        pdf_list = list(data_dir.glob("*.pdf"))
        st.markdown(f"""
        <div class="stat-card-dark">
            <div class="stat-num-glow">{len(pdf_list)}</div>
            <div class="stat-lbl">Statutory PDFs</div>
        </div>
        """, unsafe_allow_html=True)

    if pdf_list:
        with st.expander("Active Statutory Files", expanded=False):
            for pdf_f in pdf_list:
                st.caption(f"{pdf_f.name} ({pdf_f.stat().st_size // 1024} KB)")

    st.write("")
    # Re-index button
    if st.button("Re-Index Document Repository", use_container_width=True, type="primary"):
        with st.status("Re-indexing statutory repository...", expanded=True) as status:
            st.write("1. Reading PDF pages from /data...")
            pages = load_all_pdfs(str(data_dir))
            if not pages:
                st.error("No statutory PDFs detected in /data directory.")
                status.update(label="Index failed: No files found", state="error")
            else:
                st.write(f"Parsed {len(pages)} statutory page(s).")
                st.write("2. Token chunking (~500 tokens) & Section boundary detection...")
                chunks_cache = str(ROOT_DIR / "processed" / "chunks.json")
                chunks = process_pages_into_chunks(pages, chunk_size=500, overlap=100, save_to_file=chunks_cache)
                st.write(f"Generated {len(chunks)} section-tagged chunks.")
                st.write("3. Computing dense embeddings (all-MiniLM-L6-v2) & persisting to ChromaDB...")
                store.reset_collection()
                store.add_chunks(chunks)
                status.update(label="Repository indexed successfully.", state="complete")
                st.toast(f"Successfully indexed {len(chunks)} chunks into ChromaDB.")
                st.rerun()

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # 4. Viva / Architecture Reference
    with st.expander("Architecture & Viva Notes", expanded=False):
        st.markdown("""
        **Pipeline Specification**:
        - **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional dense vectors, local CPU inference)
        - **Vector Database**: `ChromaDB` (Persistent, HNSW cosine index)
        - **Inference**: Groq `llama-3.3-70b-versatile`
        - **Guardrails**: Strict context grounding, statutory section citation, refusal of out-of-scope questions, mandatory disclaimer.
        """)

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Main Page Content
# ---------------------------------------------------------
# Hero Banner
st.markdown("""
<div class="hero-banner">
    <div class="brand-row">
        <div class="brand-logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
                <path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/>
                <path d="M7 21h10"/>
                <path d="M12 3v18"/>
                <path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>
            </svg>
        </div>
        <h1 class="brand-title">DHAARA <span class="accent">AI</span></h1>
    </div>
    <div class="brand-tagline">
        Autonomous Indian Legal Research Assistant • Retrieval-Augmented Generation with Mandatory Statutory Section Citations
    </div>
    <div class="status-strip">
        <span class="status-pill"><span class="pulse-dot"></span> System: Active</span>
        <span class="status-pill">Grounding: Context-Enforced</span>
        <span class="status-pill">Citations: Statutory Sections</span>
        <span class="status-pill">Engine: Groq Llama 3.3 70B</span>
        <span class="status-pill">Vector DB: ChromaDB (Local)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Starter Suggestions (only when conversation is empty)
if len(st.session_state.messages) == 0:
    st.markdown('<div class="prompt-section-title">Select a statutory inquiry to evaluate:</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Section 420: Punishment for cheating and dishonestly inducing delivery of property", key="q1", use_container_width=True):
            st.session_state.pending_query = "What is the punishment for cheating and dishonestly inducing delivery of property under Section 420?"
            st.rerun()
        if st.button("Section 415: Essential legal elements and definition of cheating", key="q2", use_container_width=True):
            st.session_state.pending_query = "What constitutes the offense of cheating under Section 415 of the Indian Penal Code?"
            st.rerun()
    with col2:
        if st.button("Section 420: धोखाधड़ी और संपत्ति हस्तांतरण की वैधानिक सजा (Hindi)", key="q3", use_container_width=True):
            st.session_state.pending_query = "भारतीय दंड संहिता की धारा 420 के तहत धोखाधड़ी की क्या सजा निर्धारित है?"
            st.rerun()
        if st.button("Section 421: Fraudulent removal or concealment of property from creditors", key="q4", use_container_width=True):
            st.session_state.pending_query = "What are the provisions regarding dishonest removal or concealment of property under Section 421?"
            st.rerun()

# ---------------------------------------------------------
# Chat Stream History
# ---------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**{msg['content']}**")
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

            # Render source citations if available
            if msg.get("sources"):
                with st.expander(f"Statutory Authorities Cited ({len(msg['sources'])} provisions)", expanded=False):
                    for idx, src in enumerate(msg["sources"], 1):
                        relevance_pct = int(src.get("similarity_score", 0.0) * 100)
                        st.markdown(f"""
                        <div class="citation-container">
                            <div class="citation-head">
                                <span class="citation-sec-title">#{idx} | {src.get('section', 'General')} — {src.get('section_title', 'Statutory Provision')}</span>
                                <span class="match-badge">Match: {relevance_pct}%</span>
                            </div>
                            <div class="citation-meta-row">
                                <span>Act: {src.get('source', 'Unknown')}</span>
                                <span>Page: {src.get('page', 'N/A')}</span>
                            </div>
                            <div class="statutory-quote">{src.get('text', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Query Processing
# ---------------------------------------------------------
query_from_pill = st.session_state.pop("pending_query", None)
user_prompt = st.chat_input("Enter a statutory question (e.g. 'What is the penalty under Section 420?')...") or query_from_pill

if user_prompt:
    # 1. Append & render user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(f"**{user_prompt}**")

    # 2. Instantiate RAG Engine
    engine = DhaaraRAGEngine(
        embed_store=store,
        api_key=st.session_state.groq_key
    )

    # 3. Retrieve & Generate
    with st.chat_message("assistant"):
        with st.spinner("Retrieving statutory text and formulating grounded response..."):
            result = engine.query(
                question=user_prompt,
                language=current_lang,
                top_k=5,
                stream=False
            )

        answer_text = result["answer"]
        sources = result["sources"]

        # Display answer
        st.markdown(answer_text)

        # Display expandable citations
        if sources:
            with st.expander(f"Statutory Authorities Cited ({len(sources)} provisions)", expanded=True):
                for idx, src in enumerate(sources, 1):
                    relevance_pct = int(src.get("similarity_score", 0.0) * 100)
                    st.markdown(f"""
                    <div class="citation-container">
                        <div class="citation-head">
                            <span class="citation-sec-title">#{idx} | {src.get('section', 'General')} — {src.get('section_title', 'Statutory Provision')}</span>
                            <span class="match-badge">Match: {relevance_pct}%</span>
                        </div>
                        <div class="citation-meta-row">
                            <span>Act: {src.get('source', 'Unknown')}</span>
                            <span>Page: {src.get('page', 'N/A')}</span>
                        </div>
                        <div class="statutory-quote">{src.get('text', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Save to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "sources": sources
        })
