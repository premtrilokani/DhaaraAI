"""
styles.py
=========
Centralized Custom CSS for DhaaraAI to match TheLawGPT redesign.
"""
import streamlit as st

def inject_global_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Foundation */
        .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Hide Top padding and decoration */
        .main .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* SIDEBAR STYLING */
        section[data-testid="stSidebar"] {
            background-color: #F9F9F9 !important;
            border-right: 1px solid #E5E5E5 !important;
            width: 280px !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem !important;
        }
        
        /* Custom Sidebar Classes */
        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
        }
        .sidebar-logo-icon {
            width: 32px;
            height: 32px;
            background: #D94625;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .sidebar-title {
            font-size: 15px;
            font-weight: 600;
            line-height: 1.2;
            color: #111;
        }
        .sidebar-subtitle {
            font-size: 12px;
            color: #666;
        }
        .new-chat-btn {
            background: #000000;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 14px;
            font-weight: 500;
            width: 100%;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .new-chat-btn:hover {
            background: #222222;
        }
        .nav-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            color: #444;
            font-size: 13px;
            border-radius: 6px;
            cursor: pointer;
            margin-bottom: 4px;
        }
        .nav-item:hover {
            background: #EFEFEF;
        }
        .nav-item-icon {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .nav-section-title {
            font-size: 11px;
            color: #888;
            margin: 20px 0 8px 12px;
            text-transform: uppercase;
        }
        .user-profile-block {
            position: absolute;
            bottom: 20px;
            left: 16px;
            right: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
        }
        .user-profile-block:hover {
            background: #EFEFEF;
        }
        .user-avatar {
            width: 32px;
            height: 32px;
            background: #000;
            color: #fff;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 600;
        }
        
        /* MAIN CHAT AREA STYLING */
        .top-nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            border-bottom: 1px solid #EFEFEF;
        }
        .country-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border: 1px solid #E34D32;
            border-radius: 6px;
            font-size: 13px;
            color: #222;
            cursor: pointer;
        }
        .support-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #666;
            cursor: pointer;
            border: 1px solid #EEE;
            padding: 6px 12px;
            border-radius: 16px;
        }
        
        /* Central Greeting */
        .chat-greeting-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20vh;
        }
        .hello-name {
            font-size: 42px;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 24px;
            color: #111;
        }
        .unlock-pill {
            background: #F9F9F9;
            border: 1px solid #EEE;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 12px;
            color: #555;
            margin-bottom: 10px;
        }
        
        /* Chat Input Area */
        .chat-input-wrapper {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 700px;
            max-width: 90vw;
        }
        .msg-limit-text {
            text-align: right;
            font-size: 11px;
            color: #888;
            margin-bottom: 8px;
            padding-right: 12px;
        }
        .custom-chat-input {
            border: 1px solid #DDD;
            border-radius: 16px;
            padding: 16px;
            background: #FFFFFF;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .custom-input-field {
            border: none;
            outline: none;
            width: 100%;
            font-size: 15px;
            color: #222;
            resize: none;
            font-family: inherit;
        }
        .custom-input-field::placeholder {
            color: #999;
        }
        .input-actions-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .input-tools {
            display: flex;
            gap: 16px;
        }
        .input-tool-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: #777;
            cursor: pointer;
        }
        .input-tool-btn:hover {
            color: #333;
        }
        .send-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #888;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            border: none;
            cursor: pointer;
        }
        
        /* Streamlit native overrides to hide their input */
        div[data-testid="stChatInput"] {
            display: none !important;
        }
        
        /* Hide streamlit sidebar elements we replace */
        section[data-testid="stSidebar"] .stButton {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
