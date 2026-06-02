import json
from pathlib import Path

FSVO_DIR = Path("data/raw/datasets/")
PREFIX = "FSVO_D"

raw_files = sorted(FSVO_DIR.glob("*.json"))

def extract_num(path):
    name = path.stem
    if name.startswith(PREFIX):
        try:
            return int(name.replace(PREFIX, ""))
        except:
            return 0
    return 0

counter = max([extract_num(f) for f in raw_files] + [0])

for raw_file in raw_files:
    raw = json.loads(raw_file.read_text(encoding="utf-8"))

    # already correctly named → skip
    if "dct:identifier" in raw and raw["dct:identifier"].startswith(PREFIX):
        print(f"[SKIP] {raw_file.name} already has ID")
        continue

    # assign new ID
    counter += 1
    new_id = f"{PREFIX}{counter:05d}"

    old_name = raw_file.name

    raw["dct:identifier"] = new_id
    new_path = FSVO_DIR / f"{new_id}.json"

    raw_file.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")
    raw_file.rename(new_path)

    print(f"[UPDATED] {old_name} -> {new_path.name}")