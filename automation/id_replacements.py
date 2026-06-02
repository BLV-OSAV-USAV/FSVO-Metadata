import json
from pathlib import Path

FILE = Path("data/processed/datasets.json")
FSVO_DIR = Path("data/raw/datasets/")
MAP_FILE = Path("data/processed/id_map.json")
PREFIX = "FSVO_D"

# Load or initialise the map
id_map: dict[str, str] = json.loads(MAP_FILE.read_text(encoding="utf-8")) if MAP_FILE.exists() else {}

def next_id() -> str:
    n = len(id_map) + 1
    return f"{PREFIX}{n:05d}"

def assign_id(original_id: str) -> str:
    if original_id in id_map:
        return id_map[original_id]
    new_id = next_id()
    id_map[original_id] = new_id
    return new_id

data = json.loads(FILE.read_text(encoding="utf-8"))

for dataset in data:
    original_id = dataset["dct:identifier"]
    parent_id = assign_id(original_id)
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
MAP_FILE.write_text(json.dumps(id_map, indent=4, ensure_ascii=False), encoding="utf-8")
print(f"Done. {len(data)} datasets processed, {len(id_map)} total in map.")
