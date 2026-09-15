"""
sidebar.py
==========
Renders the custom TheLawGPT style sidebar using HTML.
"""
import streamlit as st

def render_sidebar():
    with st.sidebar:
        # Hide default Streamlit sidebar elements
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Inject our custom sidebar HTML
        st.markdown(f"""
        <div class="sidebar-header">
            <div class="sidebar-logo-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"></path></svg>
            </div>
            <div>
                <div class="sidebar-title">DhaaraAI</div>
                <div class="sidebar-subtitle">No subscription</div>
            </div>
        </div>

        <button class="new-chat-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            New consultation
        </button>
        """, unsafe_allow_html=True)
        
        # Native Streamlit navigation
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] .stRadio > div {
            gap: 4px;
        }
        section[data-testid="stSidebar"] .stRadio label {
            padding: 10px 12px;
            color: #444;
            font-size: 14px;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            background: transparent;
        }
        section[data-testid="stSidebar"] .stRadio label:hover {
            background: #EFEFEF;
        }
        section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] {
            color: #444 !important;
        }
        /* Hide radio circle */
        section[data-testid="stSidebar"] .stRadio div[role="radio"] > div:first-child {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)
        
        nav_selection = st.radio(
            "Navigation",
            ["Consultation", "Document Generator", "Statute Concordance", "Helplines"],
            label_visibility="collapsed"
        )
        st.session_state.current_view = nav_selection

        st.markdown(f"""
        <div class="nav-section-title">Conversations</div>

        <div class="user-profile-block">
            <div class="user-avatar">{st.session_state.user_name[:2].upper() if st.session_state.user_name else "U"}</div>
            <div style="flex: 1; overflow: hidden;">
                <div style="font-size: 13px; font-weight: 500; color: #111; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{st.session_state.user_name or "User"}</div>
                <div style="font-size: 11px; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">No active plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
