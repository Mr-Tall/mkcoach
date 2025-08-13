"""
Optional helper: prebuild embeddings to warm up caches by running the same pipeline
the app uses on first request. Not strictly required, but useful before demos.

Usage:
  python scripts/build_index.py
"""
from app.embeddings import RAGIndex

if __name__ == "__main__":
    rag = RAGIndex()
    print(f"Indexed {len(rag.docs)} items. Example hit:")
    print(rag.search("punish -14 teleport", k=3))
