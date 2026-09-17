"""
consultation.py
===============
Renders the chat interface matching TheLawGPT.
"""
import streamlit as st

def render_top_nav():
    st.markdown("""
    <div class="top-nav-bar">
        <div>
            <!-- Sidebar toggle handled by native streamlit, but we hide their button in CSS -->
        </div>
        <div class="country-selector">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
            Select jurisdiction
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </div>
        <div class="support-btn">
            Support
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_consultation_view(engine=None):
    render_top_nav()
    
    name = st.session_state.user_name.split()[0] if st.session_state.user_name else "User"
    
    # Check if there are messages
    if not st.session_state.messages:
        # Empty state with big greeting
        st.markdown(f"""
        <div class="chat-greeting-container">
            <div class="hello-name">Hello, {name}</div>
            <div class="unlock-pill">Select a jurisdiction from the top bar to unlock chat.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show chat history
        st.markdown("<div style='padding: 24px; max-width: 800px; margin: 0 auto; padding-bottom: 120px;'>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander(f"Authorities ({len(msg['sources'])})", expanded=False):
                            for idx, src in enumerate(msg["sources"], 1):
                                st.markdown(f"""
                                <div style="background: #F9F9F9; border: 1px solid #E5E5E5; padding: 12px; margin-top: 8px; border-radius: 6px;">
                                    <div style="font-size: 13px; font-weight: 600;">{src.get('section', '')}</div>
                                    <div style="font-size: 12px; color: #666; margin-top: 4px;">{src.get('text', '')}</div>
                                </div>
                                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Note: Streamlit's native st.chat_input is hidden via CSS in styles.py.
    # To truly replicate the complex input box from the screenshot, we use st.text_area with a form,
    # or just native st.chat_input if we can't fully emulate the send button cleanly in python.
    # But for a custom UI, HTML/JS injection is needed for the perfect box. Since we must run python on submit:
    
    st.markdown("<div class='chat-input-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='msg-limit-text'>3 of 3 messages left today</div>", unsafe_allow_html=True)
    
    # We use a trick: We draw the complex box visually, but we place an invisible native chat_input over it,
    # OR we use st.chat_input and just style it. 
    # Actually, styling st.chat_input is the only way to get enter-to-submit reliably in pure Streamlit.
    st.markdown("</div>", unsafe_allow_html=True)
    
    user_prompt = st.chat_input("Choose a country from the top bar to begin...")
    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Call RAG engine
        if engine:
            with st.spinner("Analyzing..."):
                result = engine.query(
                    question=user_prompt,
                    language="English",
                    user_role=st.session_state.user_role,
                    top_k=3,
                    stream=False
                )
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"]
            })
        st.rerun()

    # The custom box visual underlay:
    st.markdown("""
    <style>
    div[data-testid="stChatInput"] {
        display: block !important;
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 700px;
        max-width: 90vw;
        background: transparent !important;
    }
    div[data-testid="stChatInput"] > div {
        background: #FFFFFF !important;
        border: 1px solid #DDD !important;
        border-radius: 24px !important;
        padding: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
    }
    div[data-testid="stChatInput"] textarea {
        min-height: 50px !important;
        padding-bottom: 30px !important; /* space for tools */
    }
    /* We inject the icons via a pseudo element on the chat input container */
    div[data-testid="stChatInput"] > div::after {
        content: '📎 🔒 Web Search   🧠 Deep Reasoning';
        position: absolute;
        bottom: 18px;
        left: 20px;
        color: #888;
        font-size: 12px;
        pointer-events: none;
        white-space: pre;
    }
    </style>
    """, unsafe_allow_html=True)
