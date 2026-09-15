"""
helplines.py
============
Renders the helplines view.
"""
import streamlit as st
from real_legal_fetcher import RealLegalDataService

def render_helplines():
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 20px; font-weight: 700; color: #111; margin: 0 0 4px 0;">Official Government Helplines</h2>
        <p style="font-size: 14px; color: #666; margin: 0;">
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
            <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-size: 28px; font-weight: 700; font-family: monospace; color: #000; margin-bottom: 4px;">{h['number']}</div>
                <div style="font-size: 15px; font-weight: 600; color: #111; margin-bottom: 6px;">{h['service']}</div>
                <div style="font-size: 10px; font-weight: 700; color: #D94625; text-transform: uppercase; margin-bottom: 8px;">{h['type']}</div>
                <div style="font-size: 13px; color: #666; line-height: 1.5;">{h['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #EFEFEF; margin: 32px 0;'>", unsafe_allow_html=True)

    st.markdown('<div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #888; margin-bottom: 16px;">Citizen Safeguards under BNSS 2023</div>', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-weight: 600; color: #111; font-size: 15px; margin-bottom: 8px;">Arrest vs Section 35(3) Notice Safeguard</div>
            <ul style="font-size: 13px; color: #555; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li>For offenses punishable with imprisonment up to 7 years, routine police arrest is prohibited by statute.</li>
                <li>The Investigating Officer must issue a formal Notice of Appearance under Section 35(3) BNSS (formerly Section 41A CrPC).</li>
                <li>As long as the citizen complies with the notice and appears for questioning, arrest is barred unless specific reasons of flight risk or witness tampering are recorded in writing and submitted to the Magistrate.</li>
            </ul>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-weight: 600; color: #111; font-size: 15px; margin-bottom: 8px;">Remedy if Police Refuses to Register FIR</div>
            <ul style="font-size: 13px; color: #555; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li>Under Section 173(1) BNSS and the Supreme Court judgment in Lalita Kumari, registration of FIR is mandatory for all cognizable offenses.</li>
                <li>Zero FIR: A citizen can lodge a complaint at any police station regardless of territorial jurisdiction.</li>
                <li>Escalation: If the Station House Officer refuses, a written complaint may be sent to the Superintendent of Police under Section 173(4) BNSS.</li>
                <li>Magistrate Application: An application accompanied by an affidavit can be made before the Judicial Magistrate under Section 175(3) BNSS.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-weight: 600; color: #111; font-size: 15px; margin-bottom: 8px;">Rights of an Arrested Person</div>
            <ul style="font-size: 13px; color: #555; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li>Right to meet an advocate of choice during interrogation under Section 47 BNSS.</li>
                <li>Right to inform a relative or friend immediately upon arrest under Section 48 BNSS.</li>
                <li>Mandatory medical examination by a government medical officer under Section 53 BNSS.</li>
                <li>Mandatory production before the nearest Judicial Magistrate within 24 hours of arrest without exception.</li>
            </ul>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="font-weight: 600; color: #111; font-size: 15px; margin-bottom: 8px;">Free Legal Defense (NALSA)</div>
            <ul style="font-size: 13px; color: #555; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li>All women, children, persons in police custody, and indigent citizens are legally entitled to 100% free legal representation by government-appointed advocates.</li>
                <li>Call toll-free helpline 1516 or approach the District Legal Services Authority (DLSA) in your district court complex.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
