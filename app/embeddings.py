from sentence_transformers import SentenceTransformer
import json, os
import numpy as np
from glob import glob
from typing import List, Dict, Tuple

# Try FAISS; if not available (Windows), use scikit-learn NearestNeighbors
try:
    import faiss  # type: ignore
    USE_FAISS = True
except Exception:
    from sklearn.neighbors import NearestNeighbors
    USE_FAISS = False

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_docs(data_dir: str = "data") -> Tuple[List[str], List[Dict]]:
    docs: List[str] = []
    meta: List[Dict] = []

    # frame data
    for path in glob(os.path.join(data_dir, "frame_data", "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
        char = j.get("character", "?")
        for m in j.get("moves", []):
            txt = (
                f"{char} | {m.get('name')} | type:{m.get('type')} "
                f"startup:{m.get('startup')} on_block:{m.get('on_block')} notes:{m.get('notes','')}"
            )
            docs.append(txt)
            meta.append({
                "type": "move",
                "character": char,
                "source": path,
                "name": m.get("name")
            })

    # combos
    for path in glob(os.path.join(data_dir, "combos", "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
        char = j.get("character", "?")
        for r in j.get("routes", []):
            txt = (
                f"{char} combo {r.get('label')}: starter {r.get('starter')} "
                f"steps {r.get('steps')} dmg {r.get('damage')}"
            )
            docs.append(txt)
            meta.append({
                "type": "combo",
                "character": char,
                "source": path,
                "label": r.get("label")
            })

    # matchups
    for path in glob(os.path.join(data_dir, "matchups", "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
        txt = f"{j.get('matchup')}: notes {j.get('notes')} punishes {j.get('punishes')}"
        docs.append(txt)
        meta.append({
            "type": "matchup",
            "source": path,
            "matchup": j.get("matchup")
        })

    return docs, meta


class RAGIndex:
    def __init__(self, data_dir: str = "data"):
        self.docs, self.meta = load_docs(data_dir)
        if not self.docs:
            self.docs = ["No data loaded"]
            self.meta = [{"type": "none", "source": "", "character": ""}]

        self.model = SentenceTransformer(MODEL_NAME)
        embs = self.model.encode(self.docs, convert_to_numpy=True, normalize_embeddings=True)
        self.embs = embs.astype(np.float32)

        if USE_FAISS:
            index = faiss.IndexFlatIP(self.embs.shape[1])
            index.add(self.embs)
            self.index = index
        else:
            self.nn = NearestNeighbors(metric="cosine")
            self.nn.fit(self.embs)

    def search(self, query: str, k: int = 5):
        q = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)

        results = []
        if USE_FAISS:
            D, I = self.index.search(q, k)
            sims = D[0]
            idxs = I[0]
            for i, score in zip(idxs, sims):
                if i == -1:
                    continue
                results.append({
                    "text": self.docs[i],
                    "meta": self.meta[i],
                    "score": float(score)
                })
        else:
            distances, indices = self.nn.kneighbors(q, n_neighbors=min(k, len(self.docs)))
            for i, dist in zip(indices[0], distances[0]):
                sim = 1.0 - float(dist)
                results.append({
                    "text": self.docs[i],
                    "meta": self.meta[i],
                    "score": sim
                })

        return results
