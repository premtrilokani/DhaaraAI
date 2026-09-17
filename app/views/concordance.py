"""
concordance.py
==============
Statute concordance logic UI.
"""
import streamlit as st
from bns_concordance import CONCORDANCE_DB, lookup_by_section, search_crimes

def render_concordance():
    st.markdown("""
    <div style="background: #FFF8F6; border: 1px solid #FFE4DD; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; font-size: 14px; color: #D94625;">
        <b>Statutory Transition Rule:</b> Effective July 1, 2024, the Bharatiya Nyaya Sanhita, 2023 (BNS) replaced the Indian Penal Code, 1860 (IPC).
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        search_kw = st.text_input("Search by Section number or offense name:", placeholder="e.g. 420, 302, 318, Cheating...", label_visibility="collapsed")
    with col2:
        cat_filter = st.selectbox("Category", ["All Categories"] + sorted(list(set(c["category"] for c in CONCORDANCE_DB))), label_visibility="collapsed")

    # Filtering logic
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
        # We reuse the light mode CSS from earlier styles for concordance cards
        bail_badge = "background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0;" if "Bailable" in itm["bailable"] and "Non" not in itm["bailable"] else "background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA;"
        cog_badge = "background: #FFFBEB; color: #B45309; border: 1px solid #FDE68A;"
        
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <div style="font-size: 18px; font-weight: 600; color: #111;">{itm['offense_en']}</div>
                <div style="display: flex; gap: 8px;">
                    <span style="font-size: 11px; font-weight: 600; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; {cog_badge}">{itm['nature']}</span>
                    <span style="font-size: 11px; font-weight: 600; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; {bail_badge}">{itm['bailable']}</span>
                </div>
            </div>
            <div style="font-size: 14px; color: #666; margin-bottom: 20px;">{itm['offense_hi']} | Category: {itm['category']}</div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
                <div style="background: #F9F9F9; border: 1px solid #E5E5E5; border-radius: 8px; padding: 16px;">
                    <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #D94625; margin-bottom: 4px;">Active Law (BNS 2023)</div>
                    <div style="font-size: 16px; font-weight: 600; color: #111; font-family: monospace; margin-bottom: 4px;">Section {itm['bns_section']}</div>
                    <div style="font-size: 13px; color: #555;">{itm['bns_title']}</div>
                </div>
                <div style="background: #F9F9F9; border: 1px solid #E5E5E5; border-radius: 8px; padding: 16px;">
                    <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #888; margin-bottom: 4px;">Legacy Law (IPC 1860)</div>
                    <div style="font-size: 16px; font-weight: 600; color: #111; font-family: monospace; margin-bottom: 4px;">Section {itm['ipc_section']}</div>
                    <div style="font-size: 13px; color: #555;">{itm['ipc_title']}</div>
                </div>
            </div>

            <div style="font-size: 14px; color: #333; margin-bottom: 12px;">
                <b>Punishment:</b> {itm['punishment']} &nbsp;|&nbsp; <b>Triable by:</b> {itm['triable_by']}
            </div>

            <div style="background: #F9F9F9; padding: 12px 16px; border-radius: 8px; border: 1px solid #E5E5E5; margin-bottom: 16px; font-size: 13px; color: #444; line-height: 1.5;">
                <b style="color: #111;">Procedure:</b> {itm['bnss_procedure']}
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 13px; line-height: 1.5;">
                <div style="background: #F9F9F9; padding: 12px; border-radius: 8px; border: 1px solid #E5E5E5;">
                    <div style="font-weight: 600; color: #2563EB; margin-bottom: 4px;">For Complainant:</div>
                    <div style="color: #555;">{itm['victim_guidance']}</div>
                </div>
                <div style="background: #F9F9F9; padding: 12px; border-radius: 8px; border: 1px solid #E5E5E5;">
                    <div style="font-weight: 600; color: #B45309; margin-bottom: 4px;">For Accused:</div>
                    <div style="color: #555;">{itm['accused_guidance']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
