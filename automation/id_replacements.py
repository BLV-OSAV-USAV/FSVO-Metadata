import json
from pathlib import Path

FILE = Path("data/processed/datasets.json")
PREFIX = "FSVO_D"

data = json.loads(FILE.read_text(encoding="utf-8"))

for i, dataset in enumerate(data, start=1):
    parent_id = f"{PREFIX}{i:05d}"
    dataset["dct:identifier"] = parent_id

    for j, dist in enumerate(dataset.get("dcat:distribution", []), start=1):
        dist["dct:identifier"] = f"{parent_id}_{j}"

FILE.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
print(f"Done. Renumbered {len(data)} datasets.")