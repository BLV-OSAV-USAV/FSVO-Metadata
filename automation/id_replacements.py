import json
from pathlib import Path

FSVO_DIR = Path("data/raw/datasets/")
PREFIX = "FSVO_D"

raw_files = sorted(FSVO_DIR.glob("*.json"))

counter = 0

for raw_file in raw_files:
    raw = json.loads(raw_file.read_text(encoding="utf-8"))

    # --- dataset id from filename ---
    if raw_file.stem.startswith(PREFIX):
        dataset_id = raw_file.stem
    else:
        counter += 1
        dataset_id = f"{PREFIX}{counter:05d}"

    # ensure consistent filename ↔ id
    new_path = FSVO_DIR / f"{dataset_id}.json"

    # --- update dataset id ---
    raw["dct:identifier"] = dataset_id

    # --- update distributions ---
    distributions = raw.get("dcat:distribution", [])
    if isinstance(distributions, list):
        for i, dist in enumerate(distributions, start=1):
            if isinstance(dist, dict):
                dist["dct:identifier"] = f"{dataset_id}_{i}"

    # write file
    raw_file.write_text(
        json.dumps(raw, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    # rename if needed
    if raw_file.name != new_path.name:
        raw_file.rename(new_path)
        print(f"[RENAMED] {raw_file.name} -> {new_path.name}")
    else:
        print(f"[UPDATED] {raw_file.name}")