"""YouTube ingestion (search + download + analyze)."""

import yt_dlp
import librosa
import numpy as np
import os


def download_audio(youtube_url):
    """Extract audio only from YouTube URL and save as mp3"""
    print(f"--- '{youtube_url}' Start analysis ---")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio.%(ext)s',  # temporary file name
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return "temp_audio.mp3"


def analyze_beat(file_path):
    """Analyze audio files to extract key features"""
    print("Analyzing data...")

    # 1. 1. Load audio (sr=None maintains original sampling rate)
    y, sr = librosa.load(file_path, sr=None)

    # 2. BPM (tempo) extraction
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # 3. Calculating the average brightness of sound (Spectral Centroid)
    # This is basic data that quantifies the texture of hip-hop beats.
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_cent = np.mean(cent)

    # 4. Song length (seconds)
    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "BPM": round(float(tempo), 2),
        "Brightness": round(float(avg_cent), 2),
        "Duration": round(duration, 2)
    }


if __name__ == "__main__":
    # YouTube link for testing
    target_url = "https://www.youtube.com/watch?v=BrxZ7PsPMY0"

    try:
        audio_file = download_audio(target_url)
        results = analyze_beat(audio_file)

        print("\n" + "=" * 30)
        print(f"analysis results:")
        print(f"🥁 BPM: {results['BPM']}")
        print(f"✨ sound brightness: {results['Brightness']}")
        print(f"⏱️ length: {results['Duration']}sec")
        print("=" * 30)

        # Delete temporary files after analysis (capacity management)
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print("Temporary file deletion complete.")

    except Exception as e:
        print(f"[ERROR]: {e}")