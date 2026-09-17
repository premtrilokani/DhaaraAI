"""
test_embed_seeding.py
=====================
Quick test to verify embed_store seeding from comprehensive_statutes.json.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from embed_store import LegalEmbedStore


def test_seeding():
    print("Testing LegalEmbedStore auto-seeding...")
    store = LegalEmbedStore(db_path=str(ROOT_DIR / "chroma_db"))
    store.seed_defaults_if_empty()
    stats = store.get_stats()
    print(f"Total chunks in collection: {stats['total_chunks']}")
    assert stats["total_chunks"] >= 15, "ChromaDB should have at least 15 chunks"
    
    # Test a query
    results = store.query("cheating and online fraud", top_k=2)
    print(f"Retrieved {len(results)} chunks for 'cheating and online fraud':")
    for r in results:
        print(f"- {r['section']} ({r['section_title']}) - Score: {r['similarity_score']}")
        
    print("ALL SEEDING TESTS PASSED!")


if __name__ == "__main__":
    test_seeding()
