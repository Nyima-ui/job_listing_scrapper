import json
from pathlib import Path

jobs_file_path = Path(__file__).resolve().parent.parent / "data" / "jobs.json"


def write_in_json(jobs_list):
    try:
        with jobs_file_path.open("w", encoding="utf-8") as f:
            json.dump(jobs_list, f, indent=4, ensure_ascii=False)
    except (OSError, TypeError) as e:
        print(f"❌ Error writing to JSON file: {e}")
