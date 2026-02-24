import sys
import yt_dlp
import os
import shutil
import requests
from moviepy import VideoFileClip
from pydub import AudioSegment

def validate_inputs():
    if len(sys.argv) != 5:
        print("Usage: python <file>.py <Singer> <NumVideos> <Duration> <OutputFile>")
        sys.exit()

    singer = sys.argv[1].strip()
    if singer == "":
        print("Singer name cannot be empty.")
        sys.exit()

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print("Number of videos and duration must be integers.")
        sys.exit()

    if num_videos < 10:
        print("Number of videos must be greater than 10.")
        sys.exit()

    if duration < 20:
        print("Duration must be greater than 20 seconds.")
        sys.exit()

    try:
        requests.get("https://youtube.com", timeout=5)
    except:
        print("No internet connection.")
        sys.exit()

    output = sys.argv[4]
    return singer, num_videos, duration, output




def download(singer, num_videos):
    folder = "downloads"
    os.makedirs(folder, exist_ok=True)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'quiet': True
    }

    search_query = f"ytsearch{num_videos}:{singer} songs"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    return folder


def convert_to_mp3(folder):
    mp3_folder = "mp3"
    os.makedirs(mp3_folder, exist_ok=True)

    for file in os.listdir(folder):
        if file.endswith(".mp4"):
            path = os.path.join(folder, file)
            mp3_path = os.path.join(mp3_folder, file.split(".")[0] + ".mp3")

            video = VideoFileClip(path)
            video.audio.write_audiofile(mp3_path)
            video.close()

    return mp3_folder


def trim_audios(folder, seconds):
    trimmed_folder = "trimmed"
    os.makedirs(trimmed_folder, exist_ok=True)

    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            path = os.path.join(folder, file)
            sound = AudioSegment.from_mp3(path)
            trimmed = sound[:seconds * 1000]
            trimmed.export(os.path.join(trimmed_folder, file), format="mp3")

    return trimmed_folder


def merge_audios(folder, output_name):
    combined = AudioSegment.empty()

    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            path = os.path.join(folder, file)
            sound = AudioSegment.from_mp3(path)
            combined += sound

    combined.export(output_name, format="mp3")


def cleanup():
    folders = ["downloads", "mp3", "trimmed"]
    for f in folders:
        if os.path.exists(f):
            shutil.rmtree(f)




singer, num_videos, duration, output = validate_inputs()

try:
    print("Downloading videos...")
    folder = download(singer, num_videos)

    print("Converting to MP3...")
    mp3_folder = convert_to_mp3(folder)

    print("Trimming audio...")
    trimmed_folder = trim_audios(mp3_folder, duration)

    print("Merging files...")
    merge_audios(trimmed_folder, output)

    print("Mashup Created Successfully:", output)

except Exception as e:
    print("Error occurred:", e)

finally:
    cleanup()
