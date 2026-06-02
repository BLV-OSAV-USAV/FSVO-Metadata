import json
import re
from pathlib import Path

FSVO_DIR = Path("data/raw/datasets/")
PREFIX = "FSVO_D"

def get_existing_max(files):
    max_id = 0
    pattern = re.compile(rf"{PREFIX}(\d+)")
    
    for f in files:
        m = pattern.search(f.stem)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return max_id


raw_files = sorted(FSVO_DIR.glob("*.json"))

# find current max ID
start = get_existing_max(raw_files)

counter = start

for raw_file in raw_files:
    raw = json.loads(raw_file.read_text(encoding="utf-8"))

    # if already has ID, skip
    if "dct:identifier" in raw:
        continue

    counter += 1
    new_id = f"{PREFIX}{counter:05d}"

    raw["dct:identifier"] = new_id
    raw_file.write_text(json.dumps(raw, indent=4, ensure_ascii=False), encoding="utf-8")

    new_path = FSVO_DIR / f"{new_id}.json"
    raw_file.rename(new_path)

    print(f"{raw_file.name} -> {new_path.name}")