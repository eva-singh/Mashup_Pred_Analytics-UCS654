import streamlit as st
import yt_dlp
import os
import shutil
import requests
import zipfile
import smtplib
from email.message import EmailMessage
from moviepy import VideoFileClip
from pydub import AudioSegment

def download_videos(singer, num_videos):
    folder = "downloads"
    os.makedirs(folder, exist_ok=True)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'ignoreerrors': True
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
    return output_name


def zip_file(file_path):
    zip_name = "mashup.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(file_path)
    return zip_name


def send_email(receiver_email, zip_path):
    sender_email = "evxsingh@gmail.com"
    app_password = "oouhpijtlfaeznon" 

    msg = EmailMessage()
    msg['Subject'] = "Your Mashup is Ready!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Attached is your mashup file.")

    with open(zip_path, 'rb') as f:
        msg.add_attachment(f.read(),
                           maintype='application',
                           subtype='zip',
                           filename="mashup.zip")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)


def cleanup():
    folders = ["downloads", "mp3", "trimmed"]
    files = ["mashup.zip", "mashup.mp3"]

    for f in folders:
        if os.path.exists(f):
            shutil.rmtree(f)

    for file in files:
        if os.path.exists(file):
            os.remove(file)


st.title("Magic Mashup Generator")
st.info("Please keep this tab open until processing completes.")

singer = st.text_input("Enter Artist Name")
num_videos = st.number_input("# of videos (>=10)", min_value=10)
duration = st.number_input("duration of each video (>=20 sec)", min_value=20)
email = st.text_input("Email id")

if st.button("Generate Mashup"):

    if singer.strip() == "":
        st.error("Enter singer name")
        st.stop()

    if "@" not in email:
        st.error("Valid email required")
        st.stop()

    try:
        requests.get("https://youtube.com", timeout=5)
    except:
        st.error("No Internet")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    try:
        status.text("Downloading videos...")
        progress.progress(15)
        folder = download_videos(singer, num_videos)

        status.text("Converting to MP3...")
        progress.progress(35)
        mp3_folder = convert_to_mp3(folder)

        status.text("Trimming audio...")
        progress.progress(55)
        trimmed_folder = trim_audios(mp3_folder, duration)

        status.text("Merging audio...")
        progress.progress(70)
        final_file = merge_audios(trimmed_folder, "mashup.mp3")

        status.text("Zipping file...")
        progress.progress(85)
        zip_path = zip_file(final_file)

        status.text("Sending email...")
        progress.progress(95)
        send_email(email, zip_path)

        progress.progress(100)
        st.success("Mashup sent to email 🎉")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        cleanup()