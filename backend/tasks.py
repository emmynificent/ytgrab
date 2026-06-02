import yt_dlp
import os
import re
import uuid
from datetime import datetime

def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    filename = re.sub(r'\+', ' ', filename).strip()
    return filename


def parse_time(time_str):
    try:
        float(time_str)
        return time_str
    except ValueError:
        pass

    parts = time_str.split(":")
    if len(parts) in (2,3):
        try: 
            for part in parts:
                int(part)
            return time_str
        except ValueError:
            pass
def make_progress_hook(job_store, job_id):
    def progress_hook(d):
        if d['status'] == 'downloading':
            job_store[job_id]['progress'] = {
                'percent': d.get('_percent_str', '0%').strip(),
                'speed': d.get('_speed_str', 'N/A').strip(),
                'eta': d.get('_eta_str', 'N/A').strip()
            }
        elif d['status'] == 'finished':
            job_store[job_id]['status'] = 'processing'

    return progress_hook
def run_download(job_id, job_store, url, quality, is_playlist, starttime, endtime):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    job_store[job_id]['status'] = 'running'

    # Add Deno to PATH
    deno_path = os.path.expanduser("~/.deno/bin")
    if os.path.exists(deno_path):
        os.environ["PATH"] = deno_path + os.pathsep + os.environ.get("PATH", "")

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [make_progress_hook(job_store, job_id)],
        'ignoreerrors': True,
        'noplaylist': not is_playlist,
        'extractor_args': {
            'youtube': {
                'player_client': ['web_safari', 'ios', 'android', 'web'],
            }
        },
        'quiet': False,
        'no_warnings': False,
    }

    if starttime and endtime:
        ydl_opts['download_ranges'] = yt_dlp.utils.download_ranges_func(
            None, [(starttime, endtime)]
        )
        ydl_opts['force_keyframes_at_cuts'] = True

    if quality == "best":
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    elif quality == "1080":
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif quality == "720":
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif quality == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if info is None:
                raise Exception("Failed to extract video information. YouTube may be blocking access.")

            title = info.get('title', 'video')
            job_store[job_id]['title'] = title
            job_store[job_id]['status'] = 'completed'

    except Exception as e:
        error_msg = str(e)
        print(f"Download error: {error_msg}")
        job_store[job_id]['status'] = 'failed'
        job_store[job_id]['error'] = error_msg


