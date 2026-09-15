"""
sync_data.py
============
Script to ingest the clean IndiaCode JSON into the vector store.
Run this after replacing data/comprehensive_statutes.json
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from embed_store import LegalEmbedStore

def run_sync():
    data_dir = ROOT_DIR / "data"
    statutes_file = data_dir / "comprehensive_statutes.json"
    
    if not statutes_file.exists():
        print(f"Error: Could not find {statutes_file}")
        print("Please place your downloaded JSON file there and run this again.")
        return

    print("Initializing Legal Embed Store...")
    db_path = str(ROOT_DIR / "chroma_db")
    store = LegalEmbedStore(db_path=db_path)
    
    print("Resetting old collections...")
    store.reset_collection()
    
    print(f"Indexing clean data from {statutes_file.name}...")
    indexed_count = store.index_statutes_json(str(statutes_file))
    print(f"✅ Successfully synchronized {indexed_count} provisions into the vector database!")

if __name__ == "__main__":
    run_sync()
