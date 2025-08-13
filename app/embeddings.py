from sentence_transformers import SentenceTransformer
import faiss, json, os
import numpy as np
from glob import glob
from typing import List, Dict, Tuple

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


def build_index(docs: List[str]):
    model = SentenceTransformer(MODEL_NAME)
        return results
