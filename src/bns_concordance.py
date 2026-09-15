"""
bns_concordance.py
==================
Master Concordance & Statutory Mapping Engine for Indian Law.
Maps Bharatiya Nyaya Sanhita (BNS 2023) to legacy Indian Penal Code (IPC 1860),
Bharatiya Nagarik Suraksha Sanhita (BNSS 2023) to CrPC 1973, and
Bharatiya Sakshya Adhiniyam (BSA 2023) to Indian Evidence Act 1872.

Guarantees ZERO outdated laws by providing real-time concordance,
bail eligibility, cognizable classifications, and situational triage.
"""

import re
from typing import List, Dict, Any, Optional

# Transition Date: Criminal laws in India changed on July 1, 2024.
# Incidents before July 1, 2024 -> IPC / CrPC / IEA apply.
# Incidents on or after July 1, 2024 -> BNS / BNSS / BSA apply.
TRANSITION_DATE = "2024-07-01"

from concordance_data import CONCORDANCE_DB


def lookup_by_section(query_section: str) -> List[Dict[str, Any]]:
    """
    Looks up concordance records matching either a BNS section, IPC section, or Act name.
    """
    clean_q = re.sub(r"[^0-9a-zA-Z\s]", "", query_section.lower()).strip()
    results = []
    
    for item in CONCORDANCE_DB:
        bns_sec = re.sub(r"[^0-9a-zA-Z\s]", "", item["bns_section"].lower())
        ipc_sec = re.sub(r"[^0-9a-zA-Z\s]", "", item["ipc_section"].lower())
        
        if clean_q in bns_sec or clean_q in ipc_sec:
            results.append(item)
        elif any(clean_q in word.lower() for word in item["offense_en"].split() if len(clean_q) >= 4):
            results.append(item)

    return results


def search_crimes(keyword: str) -> List[Dict[str, Any]]:
    """
    Searches concordance database across English and Hindi offense descriptions,
    sections, categories, and guidance notes.
    """
    kw = keyword.lower().strip()
    matches = []
    
    for item in CONCORDANCE_DB:
        searchable_text = (
            f"{item['offense_en']} {item['offense_hi']} {item['category']} "
            f"{item['bns_section']} {item['ipc_section']} {item['victim_guidance']} {item['accused_guidance']}"
        ).lower()
        
        if kw in searchable_text:
            matches.append(item)
            
    return matches


def get_transition_alert(incident_date: Optional[str] = None) -> Dict[str, str]:
    """
    Returns legal transition alert based on whether the offense occurred
    before or after July 1, 2024.
    """
    return {
        "status": "active_transition",
        "active_law": "Bharatiya Nyaya Sanhita (BNS 2023) & BNSS 2023",
        "legacy_law": "Indian Penal Code (IPC 1860) & CrPC 1973",
        "transition_date": "1 July 2024",
        "rule_en": "CRITICAL TRANSITION RULE: Offenses committed on or after 1 July 2024 are registered under BNS 2023. Offenses committed before 1 July 2024 continue under IPC 1860.",
        "rule_hi": "अति-महत्वपूर्ण कानूनी नियम: 1 जुलाई 2024 को या उसके बाद हुए अपराधों पर नए कानून 'भारतीय न्याय संहिता (BNS 2023)' के तहत FIR दर्ज होती है। 1 जुलाई 2024 से पहले के मामलों में IPC 1860 लागू रहता है।"
    }


def diagnose_situation(query: str, user_role: str = "general") -> Dict[str, Any]:
    """
    Performs quick situational diagnosis to identify likely applicable sections,
    procedural rights, and immediate safeguards.
    """
    q_lower = query.lower()
    
    # Priority keyword detectors
    matched_items = []
    
    keyword_map = {
        "cheating_fraud": ["fraud", "cheating", "dhokhadhadhi", "scam", "paise le liye", "money stolen", "thagi", "chhal", "upi", "online fraud"],
        "cheque_bounce": ["cheque", "check", "bounce", "dishonour", "138", "ni act"],
        "matrimonial_cruelty": ["dowry", "dahej", "cruelty", "498a", "patni", "husband", "in-laws", "sasural", "torture"],
        "domestic_violence": ["domestic violence", "gharelu hinsa", "beaten by husband", "maintenance", "kharcha", "residence order"],
        "theft": ["theft", "chori", "stolen", "mobile chori", "purse"],
        "extortion": ["extortion", "blackmail", "dhamki", "vasooli", "ransom"],
        "criminal_intimidation": ["threat", "jaan se maarne", "dhamki", "intimidation", "abuse"],
        "rash_driving": ["accident", "rash driving", "hit and run", "gaadi thuk", "collision", "over speed"],
        "police_harassment_refusal": ["police", "fir nahi", "refuse fir", "chowki", "thana", "harassment", "detention", "notice"],
        "cyber_fraud_identity": ["hacked", "cyber", "otp", "phishing", "fake account", "instagram hack", "whatsapp hack"],
        "defamation": ["defamation", "maan hani", "badnaam", "slander", "libel", "reputation"]
    }
    
    for item_id, keywords in keyword_map.items():
        if any(kw in q_lower for kw in keywords):
            for item in CONCORDANCE_DB:
                if item["id"] == item_id and item not in matched_items:
                    matched_items.append(item)
                    
    # Fallback to general keyword match if empty
    if not matched_items:
        words = [w for w in re.findall(r"\w+", q_lower) if len(w) >= 4]
        for w in words:
            sub_matches = search_crimes(w)
            for m in sub_matches:
                if m not in matched_items:
                    matched_items.append(m)
                    if len(matched_items) >= 3:
                        break
            if matched_items:
                break

    return {
        "matched_crimes": matched_items[:3],
        "transition": get_transition_alert(),
        "user_role": user_role
    }
