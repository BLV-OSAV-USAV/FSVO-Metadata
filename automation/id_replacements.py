import json
from pathlib import Path

FSVO_DIR = Path("data/raw/datasets/")
PREFIX = "FSVO_D"

counter = 0

for raw_file in sorted(FSVO_DIR.glob("*.json")):
    raw = json.loads(raw_file.read_text(encoding="utf-8"))

    if raw_file.stem.startswith(PREFIX):
        dataset_id = raw_file.stem
    else:
        counter += 1
        dataset_id = f"{PREFIX}{counter:05d}"

    raw["dct:identifier"] = dataset_id

    for i, dist in enumerate(raw.get("dcat:distribution", []), start=1):
        if isinstance(dist, dict):
            dist["dct:identifier"] = f"{dataset_id}_{i}"

    raw_file.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")

    new_path = FSVO_DIR / f"{dataset_id}.json"
    if raw_file.name != new_path.name:
        raw_file.rename(new_path)
        print(f"[RENAMED] {raw_file.name} -> {new_path.name}")
    else:
        print(f"[UPDATED] {raw_file.name}")