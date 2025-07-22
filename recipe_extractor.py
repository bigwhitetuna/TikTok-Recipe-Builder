import yt_dlp
import sys
import json
from pathlib import Path
import moviepy

def create_output_dirs(video_id):
    base = Path("downloads") / video_id / "assets"
    base.mkdir(parents=True, exist_ok=True)
    return base

def download_tiktok_video(url, video_id, output_dir):
    
    ydl_opts = {
        "outtmpl": str(output_dir / f"{video_id}.%(ext)s"),
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

def extract_audio(video_path, audio_path):
    clip = moviepy.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    

### Uses local version of whisper
import whisper

def transcribe_audio_locally(audio_path, output_dir, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(str(audio_path))
    
    transcript = result["text"]
    
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"✅ Transcript saved to {output_dir}")
    return transcript

# Uses OpenAI's API
# import openai
# Need to have OPENAI_API_KEY defined in environment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

# client = openai.OpenAI()

# def transcribe_audio(audio_path, output_path):
#     with open(audio_path, "rb") as f:
#         response = client.audio.transcriptions.create(
#             model="whisper-1",
#             file=f
#         )
    
#     transcript = response.text

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(transcript)

#     print(f"✅ Transcript saved to {output_path}")
#     return transcript

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("Usage: python recipe_extractor.py <tiktok_url>")
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
    
    video_path = output_dir / f"{video_id}.mp4"
    audio_path = output_dir / f"{video_id}.wav"
    transcript_path = output_dir / f"{video_id}_transcript.txt"

    print("🎧 Extracting audio...")
    extract_audio(video_path, audio_path)

    print("🗣️ Transcribing audio with Whisper (local)...")
    transcript = transcribe_audio_locally(audio_path, transcript_path)
    
    recipe_info = {
        "title": title,
        "description": desc,
        "transcript": transcript,
    }
    
    recipe_info_path = Path("downloads") / video_id / "recipe_info.json"
    with open(recipe_info_path, "w", encoding="utf-8") as f:
        json.dump(recipe_info, f, indent=2)
        
    print(f"📦 Bundled metadata and transcript into {recipe_info_path}")