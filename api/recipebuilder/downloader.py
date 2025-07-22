import yt_dlp
from pathlib import Path

def download_audio(url, output_base_dir="downloads"):
    ydl_opts = {
        "format": "bestaudio/best",
        "writeinfojson": True,
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",  # Best quality
            }
        ],
        "outtmpl": str(Path(output_base_dir) / "%(id)s" / "assets" / "%(id)s.%(ext)s"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # If it's a playlist, info is a "playlist result"
        if "entries" in info:
            downloaded = []
            for entry in info["entries"]:
                if entry:  # Some entries might be None (e.g. deleted videos)
                    downloaded.append(entry)
            return downloaded  # List of video metadata dicts
        else:
            return [info]  # Just a single video, wrapped in a list
        

# def create_output_dirs(video_id):
#     base = Path("downloads") / video_id / "assets"
#     base.mkdir(parents=True, exist_ok=True)
#     return base