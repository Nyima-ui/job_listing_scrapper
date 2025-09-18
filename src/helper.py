import os
import json

helper_dir = os.path.dirname(os.path.abspath(__file__))
jobs_file_path = os.path.join(helper_dir, os.pardir, "data", "jobs.json")


def write_in_json(jobs_list):
    with open(jobs_file_path, "w", encoding="utf-8") as f:
        json.dump(jobs_list, f, indent=4)
