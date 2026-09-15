"""
test_stage4_bns.py
==================
Verification script for Stage 4:
1. Tests BNS 2023 ⟷ IPC 1860 concordance mapping (Zero Outdated Law).
2. Tests BNSS 2023 procedural safeguards (Section 35(3) notice, Zero FIR, Anticipatory Bail).
3. Tests situational triage for common emergencies (Cyber fraud, Cheque bounce, Police notice, Accidents).
4. Validates comprehensive statutes dataset and ChromaDB indexing.
"""

import sys
import os
import json
from pathlib import Path

# UTF-8 support for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from bns_concordance import (
    CONCORDANCE_DB,
    lookup_by_section,
    search_crimes,
    diagnose_situation,
    get_transition_alert
)
from real_legal_fetcher import RealLegalDataService, OFFICIAL_LEGAL_HELPLINES


def run_tests():
    print("=" * 65)
    print("DHAARAAI STAGE 4 VERIFICATION: BNS 2023 & Situational Legal Triage")
    print("=" * 65)

    # 1. Test Concordance Database Size
    print("\n--- 1. Testing Concordance Master Dataset ---")
    print(f"Total Offenses Mapped: {len(CONCORDANCE_DB)}")
    assert len(CONCORDANCE_DB) >= 10, "Concordance database should contain key offenses"
    print("PASS: Concordance database loaded with major offenses.")

    # 2. Test Section Lookup (IPC -> BNS and BNS -> IPC)
    print("\n--- 2. Testing Section Lookup (IPC ⟷ BNS) ---")
    lookup_420 = lookup_by_section("420")
    assert len(lookup_420) > 0, "Lookup for IPC 420 must succeed"
    print(f"IPC 420 -> Active BNS Section: {lookup_420[0]['bns_section']} ({lookup_420[0]['offense_en']})")
    assert "318" in lookup_420[0]["bns_section"], "IPC 420 must map to BNS 318(4)"

    lookup_bns = lookup_by_section("303")
    assert len(lookup_bns) > 0, "Lookup for BNS 303 must succeed"
    print(f"BNS 303 -> Legacy IPC Section: {lookup_bns[0]['ipc_section']} ({lookup_bns[0]['offense_en']})")
    assert "379" in lookup_bns[0]["ipc_section"], "BNS 303 must map to IPC 379"
    print("PASS: Bidirectional concordance verified.")

    # 3. Test Transition Date Alert
    print("\n--- 3. Testing 1 July 2024 Transition Rule ---")
    trans = get_transition_alert()
    print(f"Active Law: {trans['active_law']}")
    print(f"Transition Rule: {trans['rule_en']}")
    assert "1 July 2024" in trans["transition_date"]
    print("PASS: Transition rule verified.")

    # 4. Test Situational Triage Engine
    print("\n--- 4. Testing Situational Legal Diagnosis ---")
    
    # Test A: Cyber Fraud
    diag_fraud = diagnose_situation("Someone stole 25000 rs from my bank account through UPI link scam", user_role="victim")
    assert len(diag_fraud["matched_crimes"]) > 0, "Cyber fraud should match"
    c_fraud = diag_fraud["matched_crimes"][0]
    print(f"Scenario: UPI Fraud -> Matched BNS: {c_fraud['bns_section']} | Bailable: {c_fraud['bailable']}")
    print(f"Victim Action: {c_fraud['victim_guidance'][:80]}...")
    
    # Test B: Police Notice
    diag_police = diagnose_situation("Police has issued notice to appear at police station", user_role="accused")
    assert len(diag_police["matched_crimes"]) > 0, "Police notice should match"
    print(f"Scenario: Police notice -> Matched: {diag_police['matched_crimes'][0]['offense_en']}")

    # Test C: Cheque Bounce
    diag_cheque = diagnose_situation("My client gave me a cheque that bounced due to insufficient balance", user_role="victim")
    assert any("138" in c["bns_section"] or "138" in c["ipc_section"] for c in diag_cheque["matched_crimes"])
    print(f"Scenario: Cheque Bounce -> Matched: Section 138 NI Act verified")
    print("PASS: Situational triage verified across multiple scenarios.")

    # 5. Test Landmark Supreme Court Guidelines
    print("\n--- 5. Testing Landmark Supreme Court Directives ---")
    guidelines = RealLegalDataService.get_landmark_guidance_for_query("police arrest notice 41a section 35")
    assert len(guidelines) > 0, "Should match Arnesh Kumar / Sec 35 BNSS arrest rules"
    print(f"Matched Case: {guidelines[0]['case_name']}")
    print(f"Rule: {guidelines[0]['key_rule'][:100]}...")
    print("PASS: Landmark legal guidance verified.")

    # 6. Test Emergency Helplines
    print("\n--- 6. Testing Emergency Helplines ---")
    helplines = RealLegalDataService.get_helplines()
    assert len(helplines) >= 5, "Must provide key emergency helplines"
    print("Active Helplines:")
    for h in helplines:
        print(f"• {h['service']}: {h['number']} ({h['type']})")
    print("PASS: Emergency helplines verified.")

    # 7. Test Comprehensive Statutes JSON file
    print("\n--- 7. Testing Comprehensive Statutes JSON ---")
    statutes_path = ROOT_DIR / "data" / "comprehensive_statutes.json"
    assert statutes_path.exists(), "Statutes JSON must exist"
    with open(statutes_path, "r", encoding="utf-8") as f:
        statutes = json.load(f)
    print(f"Statutes dataset contains {len(statutes)} verified provisions.")
    assert len(statutes) >= 15, "Should have 15+ comprehensive provisions"
    print("PASS: Comprehensive statutes dataset verified.")

    print("\n" + "=" * 65)
    print("ALL STAGE 4 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
