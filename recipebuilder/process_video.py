import sys
from pathlib import Path
from recipebuilder.downloader import create_output_dirs, download_tiktok_video
from recipebuilder.metadata import get_description_from_info_file
from recipebuilder.audio import extract_audio, transcribe_audio_locally
from recipebuilder.recipe import bundle_recipe_info

def process_video(url: str):
    if len(sys.argv) < 2:
        print("Usage: python main.py <tiktok_url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"🔗 Downloading TikTok video and metadata from:\n{url}")

    video_id = url.rstrip("/").split("/")[-1]
    output_dir = create_output_dirs(video_id)
    info = download_tiktok_video(url, video_id, output_dir)

    info_file = output_dir / f"{video_id}.info.json"
    if info_file.exists():
        desc, title = get_description_from_info_file(info_file)
        print(f"\n📝 Title: {title}\n")
        print(f"\n📋 Description:\n{desc}\n")
    else:
        print(f"❌ Metadata file not found.")
        sys.exit(1)

    video_path = output_dir / f"{video_id}.mp4"
    audio_path = output_dir / f"{video_id}.wav"
    transcript_path = output_dir / f"{video_id}_transcript.txt"

    print("🎧 Extracting audio...")
    extract_audio(video_path, audio_path)

    print("🗣️ Transcribing audio with Whisper (local)...")
    transcript = transcribe_audio_locally(audio_path, transcript_path)

    bundle_recipe_info(video_id, title, desc, transcript)