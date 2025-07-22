import json
from pathlib import Path

def get_description_from_info_file(info_file_path):
    with open(info_file_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return metadata.get("description", ""), metadata.get("title", "Untitled")