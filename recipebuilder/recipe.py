import json
from pathlib import Path

def bundle_recipe_info(video_id, title, description, transcript, url):
    recipe_info = {
        "title": title,
        "description": description,
        "transcript": transcript,
        "url": url,
    }
    recipe_info_path = Path("downloads") / video_id / "recipe_info.json"
    with open(recipe_info_path, "w", encoding="utf-8") as f:
        json.dump(recipe_info, f, indent=2)
    print(f"📦 Bundled metadata and transcript into {recipe_info_path}")