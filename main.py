import sys

from recipebuilder.process_video import process_video

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <tiktok_url")
        sys.exit(1)
        
    url = sys.argv[1]
    process_video(url)