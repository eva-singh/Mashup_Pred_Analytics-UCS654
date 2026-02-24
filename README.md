# Mashup Assignment

This project implements a **Song Mashup Generator** using Python.  
It consists of two parts:
1. **Command Line Interface (CLI) Program**
2. **Web Service Application**

The program downloads songs of a given singer from YouTube, extracts audio, trims clips, merges them into a mashup, and sends the result via email.

## Requirements

- Python **3.11** (recommended)
- FFmpeg
- Internet connection
- 
All required libraries are listed in `requirements.txt`.
pip install -r requirements.txt

## Email Configuration
Email Configuration
The application uses Gmail SMTP with an App Password.

## Program 1 — CLI Mashup Generator
to run: python 102317129.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFile>
## Program 2 — Web Service
to run: streamlit run app.py

