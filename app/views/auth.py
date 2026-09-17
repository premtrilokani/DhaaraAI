"""
auth.py
=======
Sign in component for DhaaraAI, matching the pristine look.
"""
import streamlit as st

def render_auth():
    st.markdown("""
    <div style="max-width: 400px; margin: 10vh auto; padding: 40px 30px; background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: center; margin-bottom: 24px;">
            <div style="width: 48px; height: 48px; background: #D94625; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"></path></svg>
            </div>
        </div>
        <h2 style="font-size: 24px; font-weight: 700; color: #111; text-align: center; margin-bottom: 8px;">Welcome back</h2>
        <p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 32px;">
            Enter your details to access statutory intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            name = st.text_input("Full Name", placeholder="e.g. Rajesh Kumar")
            age = st.number_input("Age", min_value=18, max_value=120, value=25)
            
            st.markdown("""
            <style>
            div[data-testid="stForm"] button {
                background: #000000 !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                padding: 12px !important;
            }
            div[data-testid="stForm"] button:hover {
                background: #222 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            submit = st.form_submit_button("Continue", use_container_width=True)
            
            if submit:
                if not name.strip():
                    st.error("Please enter your name.")
                else:
                    st.session_state.user_name = name.strip()
                    st.session_state.user_age = age
                    st.session_state.logged_in = True
                    st.rerun()
