"""
landing.py
==========
Renders the public landing page mimicking TheLawGPT.com.
"""
import streamlit as st

def render_landing():
    # Inject landing specific styles
    st.markdown("""
    <style>
    .landing-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px 60px 20px;
        background-color: #FFFFFF;
    }
    .hero-badge {
        background: #F0F0F0;
        color: #333;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 24px;
        border: 1px solid #E5E5E5;
    }
    .hero-title {
        font-size: 56px;
        font-weight: 700;
        color: #111;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin-bottom: 24px;
        max-width: 800px;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #666;
        line-height: 1.5;
        max-width: 600px;
        margin-bottom: 40px;
    }
    .hero-buttons {
        display: flex;
        gap: 16px;
        margin-bottom: 60px;
    }
    .btn-primary {
        background: #000;
        color: #fff;
        padding: 14px 28px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        text-decoration: none;
        border: none;
        cursor: pointer;
    }
    .btn-secondary {
        background: #fff;
        color: #000;
        padding: 14px 28px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        border: 1px solid #CCC;
        text-decoration: none;
        cursor: pointer;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px 80px 20px;
    }
    .feature-card {
        background: #F9F9F9;
        border: 1px solid #EFEFEF;
        border-radius: 16px;
        padding: 32px;
        text-align: left;
    }
    .feature-icon {
        width: 40px;
        height: 40px;
        background: #000;
        color: #fff;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .feature-title {
        font-size: 18px;
        font-weight: 600;
        color: #111;
        margin-bottom: 12px;
    }
    .feature-desc {
        font-size: 14px;
        color: #666;
        line-height: 1.5;
    }
    </style>
    
    <div class="landing-hero">
        <div class="hero-badge">DhaaraAI — Autonomous Legal Intelligence</div>
        <div class="hero-title">Your AI co-counsel for Indian Law.</div>
        <div class="hero-subtitle">
            Navigate the Bharatiya Nyaya Sanhita (BNS 2023) and legacy IPC seamlessly. 
            Generate drafts, analyze cases, and find statutory concordance in seconds.
        </div>
    </div>
    
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            </div>
            <div class="feature-title">Statute Concordance</div>
            <div class="feature-desc">Instantly map legacy IPC sections to the new BNS 2023 provisions with complete procedural guidance.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            </div>
            <div class="feature-title">Document Generator</div>
            <div class="feature-desc">Draft Section 173 BNSS FIR applications and Section 138 NI Act notices automatically.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <div class="feature-title">Deep Case Search</div>
            <div class="feature-desc">Ask complex legal questions and get highly factual, citation-backed responses.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; margin-bottom: 40px;'><h3 style='font-size: 24px; font-weight: 700;'>Get Started</h3></div>", unsafe_allow_html=True)
    
    from views.auth import render_auth
    render_auth()
