import json
import hashlib
from pathlib import Path

FILE = Path("data/processed/datasets.json")
FSVO_DIR = Path("data/raw/datasets/FSVO")
PREFIX = "FSVO_D"

seen: dict[str, str] = {}

def stable_id(original_id: str) -> str:
    if original_id.startswith(PREFIX):
        return original_id
    number = int(hashlib.md5(original_id.encode()).hexdigest(), 16) % 90000 + 10000
    new_id = f"{PREFIX}{number:05d}"
    if new_id in seen and seen[new_id] != original_id:
        raise ValueError(f"Hash collision: {new_id} claimed by both '{seen[new_id]}' and '{original_id}'")
    seen[new_id] = original_id
    return new_id

data = json.loads(FILE.read_text(encoding="utf-8"))

for dataset in data:
    original_id = dataset["dct:identifier"]
    parent_id = stable_id(original_id)
    dataset["dct:identifier"] = parent_id

    raw_file = FSVO_DIR / f"{original_id}.json"
    if raw_file.exists():
        raw = json.loads(raw_file.read_text(encoding="utf-8"))
        raw["dct:identifier"] = parent_id
        new_raw_file = FSVO_DIR / f"{parent_id}.json"
        raw_file.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")
        raw_file.rename(new_raw_file)

    for j, dist in enumerate(dataset.get("dcat:distribution", []), start=1):
        original_dist_id = dist["dct:identifier"]
        new_dist_id = f"{parent_id}_{j}"
        dist["dct:identifier"] = new_dist_id

        raw_dist = FSVO_DIR / f"{original_dist_id}.json"
        if raw_dist.exists():
            raw = json.loads(raw_dist.read_text(encoding="utf-8"))
            raw["dct:identifier"] = new_dist_id
            new_raw_dist = FSVO_DIR / f"{new_dist_id}.json"
            raw_dist.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")
            raw_dist.rename(new_raw_dist)

FILE.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
print(f"Done. Renumbered {len(data)} datasets.")
