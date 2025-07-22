from moviepy import VideoFileClip
import whisper


def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

def transcribe_audio_locally(audio_path, transcript_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(str(audio_path))
    transcript = result["text"]

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"✅ Transcript saved to {transcript_path}")
    return transcript