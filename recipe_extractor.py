import yt_dlp
import os
import sys
import json
from pathlib import Path

def download_tiktok_video(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        "writeinfojson": True,
        "quiet": False, # set to true if you want to suppress output
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info # contains metadata

def get_description_from_info_file(info_file_path):
    with open(info_file_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return metadata.get("description", ""), metadata.get("title", "Untitled")

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("Usage: python recipe_extractor.py <tiktok_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"🔗 Downloading TikTok video and metadata from:\n{url}")
    
    info = download_tiktok_video(url)
    video_id = info["id"]
    info_file = Path(f"downloads/{video_id}.info.json")
    
    if info_file.exists():
        desc, title = get_description_from_info_file(info_file)
        print(f"\n📝 Title: {title}\n")
        print(f"\n📋 Decsription:\n{desc}\n")
    else:
        print(f"❌ Metadata file not found.")