import sys
from pathlib import Path
from recipebuilder.downloader import download_audio
from recipebuilder.audio import transcribe_audio_locally
from recipebuilder.recipe_object_bundler import bundle_recipe_info

def process_video(url: str):
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_or_playlist_url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"🔗 Downloading audio and metadata from:\n{url}")

    infos = download_audio(url)  # Returns a list of video info dicts

    for info in infos:
        video_id = info["id"]
        title = info.get("title", "")
        desc = info.get("description", "")

        output_dir = Path("downloads") / video_id / "assets"
        info_file = output_dir / f"{video_id}.info.json"
        audio_path = output_dir / f"{video_id}.wav"
        transcript_path = output_dir / f"{video_id}_transcript.txt"

        print(f"\n📝 Title: {title}\n")
        print(f"\n📋 Description:\n{desc}\n")

        if not audio_path.exists():
            print(f"❌ Audio file not found: {audio_path}")
            continue

        print("🗣️ Transcribing audio with Whisper (local)...")
        transcript = transcribe_audio_locally(audio_path, transcript_path)

        bundle_recipe_info(video_id, title, desc, transcript, url)