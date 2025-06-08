from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import shutil
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "No playlist URL provided"

    folder_id = str(uuid.uuid4())
    download_path = f"downloads/{folder_id}"
    os.makedirs(download_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        zip_path = shutil.make_archive(download_path, 'zip', download_path)
        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"
