import json
import hashlib
from pathlib import Path

FILE = Path("data/processed/datasets.json")
PREFIX = "FSVO_D"

def stable_id(original_id: str) -> str:
    number = int(hashlib.md5(original_id.encode()).hexdigest(), 16) % 90000 + 10000
    return f"{PREFIX}{number:05d}"

data = json.loads(FILE.read_text(encoding="utf-8"))

for dataset in data:
    original_id = dataset["dct:identifier"]
    parent_id = stable_id(original_id)
    dataset["dct:identifier"] = parent_id

    for j, dist in enumerate(dataset.get("dcat:distribution", []), start=1):
        dist["dct:identifier"] = f"{parent_id}_{j}"

FILE.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
print(f"Done. Renumbered {len(data)} datasets.")