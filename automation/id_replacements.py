import json
from pathlib import Path

FSVO_DIR = Path("data/raw/datasets/")
PREFIX = "FSVO_D"

raw_files = sorted(FSVO_DIR.glob("*.json"))

for i, raw_file in enumerate(raw_files, start=1):
    new_id = f"{PREFIX}{i:05d}"
    raw = json.loads(raw_file.read_text(encoding="utf-8"))
    raw["dct:identifier"] = new_id
    raw_file.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")
    raw_file.rename(FSVO_DIR / f"{new_id}.json")
    print(f"{raw_file.name} -> {new_id}.json")
