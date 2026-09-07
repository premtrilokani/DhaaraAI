"""
test_stage2.py
==============
Verification script for Stage 2:
1. Tests local sentence-transformers (all-MiniLM-L6-v2) embedding generation
2. Tests persistent ChromaDB storage in chroma_db/
3. Tests storing chunks with section, source, page metadata
4. Tests vector similarity retrieval with sample legal questions
"""

import sys
import os
import json
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from embed_store import LegalEmbedStore


def run_stage2_verification():
    print("=" * 65)
    print("DHAARAAI STAGE 2 VERIFICATION: Embeddings & ChromaDB Storage")
    print("=" * 65)

    # Step 1: Check for chunks in processed/chunks.json
    chunks_path = Path("processed/chunks.json")
    if not chunks_path.exists():
        print("[test_stage2] 'processed/chunks.json' not found. Running stage 1 chunker first...")
        from test_stage1 import run_stage1_verification
        run_stage1_verification()

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"\n-> Loaded {len(chunks)} chunk(s) from '{chunks_path}'.")

    # Step 2: Initialize LegalEmbedStore (loads model + connects to ChromaDB)
    print("\n--- 1. Initializing Local Embedding Model & Persistent ChromaDB ---")
    store = LegalEmbedStore(db_path="chroma_db")

    # Step 3: Index chunks into ChromaDB
    print("\n--- 2. Storing Chunks with Embeddings & Metadata ---")
    indexed_count = store.add_chunks(chunks)
    print(f"-> Upserted {indexed_count} chunk(s) into ChromaDB.")

    # Step 4: Verify collection statistics
    stats = store.get_stats()
    print("\n--- 3. Collection Statistics ---")
    print(f"  • Collection Name: {stats['collection_name']}")
    print(f"  • Total Chunks   : {stats['total_chunks']}")
    print(f"  • Unique Sources : {stats['unique_sources']}")
    print(f"  • Embedding Model: {stats['model_name']}")
    print(f"  • DB Directory   : {stats['db_path']}")

    # Step 5: Test Semantic Similarity Search Queries
    test_queries = [
        "What is the punishment for cheating and dishonestly inducing delivery of property?",
        "What constitutes the offense of cheating?",
        "What happens if someone conceals property to prevent distribution among creditors?"
    ]

    print("\n--- 4. Testing Semantic Similarity Retrieval (Top Chunks) ---")
    for idx, q in enumerate(test_queries, 1):
        print(f"\n[Query #{idx}]: \"{q}\"")
        results = store.query(q, top_k=2)

        for rank, r in enumerate(results, 1):
            print(f"   Rank {rank} (Score: {r['similarity_score']}):")
            print(f"     • Section     : {r['section']} - {r['section_title']}")
            print(f"     • Source      : {r['source']} (Page {r['page']})")
            print(f"     • Chunk ID    : {r['chunk_id']}")
            print(f"     • Text Snippet: {r['text'][:120]}...")

    print("\n" + "=" * 65)
    print("STAGE 2 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_stage2_verification()
