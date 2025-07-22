import yt_dlp
from pathlib import Path

def download_tiktok_video(url, video_id, output_dir):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / f"{video_id}.%(ext)s"),
        "writeinfojson": True,
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0", # Best quality
            }
        ]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info

def create_output_dirs(video_id):
    base = Path("downloads") / video_id / "assets"
    base.mkdir(parents=True, exist_ok=True)
    return base