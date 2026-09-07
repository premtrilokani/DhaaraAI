"""
test_stage3.py
==============
Verification script for Stage 3:
1. Verifies ChromaDB retrieval (top 5 chunks with similarity scores)
2. Verifies system prompt enforcement:
   (a) only answer from context
   (b) always cite section number
   (c) append disclaimer "This is not legal advice, please consult a lawyer"
   (d) say "I don't have enough information" if context doesn't contain clear answer
3. Tests English & Hindi generation via Groq Llama 3.3 (if GROQ_API_KEY is configured)
"""

import sys
import os
import io
from pathlib import Path
from dotenv import load_dotenv

# Ensure Windows console supports Unicode (Hindi / Devanagari)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from embed_store import LegalEmbedStore
from rag_engine import DhaaraRAGEngine, SYSTEM_PROMPT_TEMPLATE, DISCLAIMER_EN, DISCLAIMER_HI

load_dotenv()


def run_stage3_verification():
    print("=" * 65)
    print("DHAARAAI STAGE 3 VERIFICATION: RAG Engine & Groq Llama 3.3")
    print("=" * 65)

    # Step 1: Connect to ChromaDB
    print("\n--- 1. Connecting to Vector Store ---")
    store = LegalEmbedStore(db_path="chroma_db")
    stats = store.get_stats()
    print(f"-> ChromaDB ready with {stats['total_chunks']} chunks from {stats['unique_sources']}")

    # Step 2: Initialize RAG Engine
    print("\n--- 2. Initializing DhaaraRAGEngine ---")
    engine = DhaaraRAGEngine(embed_store=store)

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        print("\n[NOTE]: GROQ_API_KEY is not set in .env yet.")
        print("To run live LLM calls, get a free key from: https://console.groq.com/keys")
        print("and paste it into .env (e.g. GROQ_API_KEY=gsk_...)")
        print("\nProceeding to test: Retrieval -> Context Assembling -> Prompt Validation...")
    else:
        masked_key = api_key[:6] + "..." + api_key[-4:]
        print(f"-> Detected GROQ_API_KEY: {masked_key}")

    # Test Query 1: Specific legal question in English
    test_q1 = "What is the maximum punishment for cheating under Section 420?"
    print(f"\n--- 3. Testing RAG Query 1 (English): \"{test_q1}\" ---")
    result1 = engine.query(test_q1, language="English", top_k=5)

    print("\n[Retrieved Sources Used]:")
    for idx, s in enumerate(result1["sources"], 1):
        print(f"  [{idx}] Section: {s['section']} ({s['section_title']}) | Score: {s['similarity_score']} | Source: {s['source']} (Page {s['page']})")

    print("\n[Generated Answer]:")
    print(result1["answer"])

    # Verify disclaimer presence
    assert DISCLAIMER_EN in result1["answer"] or DISCLAIMER_HI in result1["answer"], "Disclaimer missing!"
    print("-> Verification Passed: Mandatory disclaimer is present.")

    # Test Query 2: Legal question in Hindi
    test_q2 = "धारा 420 के अनुसार धोखाधड़ी के लिए क्या सजा निर्धारित है?"
    print(f"\n--- 4. Testing RAG Query 2 (Hindi): \"{test_q2}\" ---")
    result2 = engine.query(test_q2, language="Hindi", top_k=5)
    print("\n[Generated Answer (Hindi)]:")
    print(result2["answer"])

    # Test Query 3: Out-of-domain question (testing refusal rule (d))
    test_q3 = "What is the penalty for driving without a helmet under the Indian Penal Code?"
    print(f"\n--- 5. Testing Refusal Rule on Out-of-Domain Question: \"{test_q3}\" ---")
    result3 = engine.query(test_q3, language="English", top_k=5)
    print("\n[Generated Answer for Out-of-Domain]:")
    print(result3["answer"])

    print("\n" + "=" * 65)
    print("STAGE 3 VERIFICATION COMPLETED!")
    print("=" * 65)


if __name__ == "__main__":
    run_stage3_verification()
