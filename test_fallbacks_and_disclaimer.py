"""
test_fallbacks_and_disclaimer.py
================================
Verifies:
1. Mandatory legal disclaimer presence.
2. Vector search threshold fallback ('Iske liye specific statute nahi mila, general guidance:').
3. Graceful degradation on Groq API failure/offline mode without crash.
4. Clean IndiaCode source attribution.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from rag_engine import DhaaraRAGEngine, LEGAL_DISCLAIMER
from embed_store import LegalEmbedStore


def run_tests():
    print("=" * 65)
    print("TESTING FALLBACKS, DISCLAIMER, AND INDIACODE SOURCE ATTRIBUTION")
    print("=" * 65)

    store = LegalEmbedStore(db_path=str(ROOT_DIR / "chroma_db"))
    store.reset_collection()
    store.index_statutes_json(str(ROOT_DIR / "data" / "comprehensive_statutes.json"))
    engine = DhaaraRAGEngine(embed_store=store)

    # 1. Test Mandatory Disclaimer
    print("\n--- 1. Testing Mandatory Disclaimer ---")
    expected_disclaimer = "Ye legal information hai, professional legal advice ka substitute nahi. Kisi advocate se consult karein."
    assert LEGAL_DISCLAIMER == expected_disclaimer, f"Expected disclaimer to match exactly"
    print(f"PASS: Legal disclaimer string verified:\n'{LEGAL_DISCLAIMER}'")

    # 2. Test Offline / Groq API Exception Graceful Fallback
    print("\n--- 2. Testing Graceful API / Offline Fallback ---")
    # Simulate query without Groq client
    engine.client = None
    engine.api_key = ""
    res = engine.query("Someone cheated me online with UPI", user_role="victim")
    
    assert "answer" in res, "Should return an answer"
    print(f"Fallback response received (Length: {len(res['answer'])} chars)")
    assert LEGAL_DISCLAIMER in res["answer"], "Mandatory disclaimer must be in fallback response"
    print("PASS: Offline fallback works cleanly without crashing and contains mandatory disclaimer.")

    # 3. Test Vector Threshold Fallback
    print("\n--- 3. Testing Vector Similarity Threshold Fallback ---")
    # Query completely unrelated to statutory provisions
    irrelevant_query = "quantum physics entanglement superstring cosmological constant"
    res_irrelevant = engine.query(irrelevant_query, user_role="general")
    assert "Iske liye specific statute nahi mila, general guidance:" in res_irrelevant["answer"], \
        "Must contain vector fallback message when no relevant statute is matched"
    assert LEGAL_DISCLAIMER in res_irrelevant["answer"], "Disclaimer must be present"
    print("PASS: Vector threshold fallback verified with expected message.")

    # 4. Test Clean IndiaCode Source Attribution
    print("\n--- 4. Testing IndiaCode Clean Source Attribution ---")
    chunks = store.query("Cheating", top_k=1)
    assert len(chunks) > 0, "Should retrieve chunks"
    source = chunks[0]["source"]
    print(f"Retrieved Source: '{source}'")
    assert "IndiaCode" in source, "Source must attribute IndiaCode"
    print("PASS: Clean IndiaCode source attribution verified.")

    print("\n" + "=" * 65)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
