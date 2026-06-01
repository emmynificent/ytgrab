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

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [make_progress_hook(job_store, job_id)],
        'ignoreerrors': True,
        'noplaylist': not is_playlist,
        'cookiefile': 'cookies.txt'
    }

    if starttime and endtime:
         ydl_opts['download_ranges'] = yt_dlp.utils.download_ranges_func(
        None, [(starttime, endtime)]
        ) 
         ydl_opts['force_keyframes_at_cuts'] = True

    if quality == "best":
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]  
    elif quality == "1080":
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    elif quality == "720":
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]  
    elif quality == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try: 
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting download for job {job_id} with URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                raise Exception("Could not fetch video info. Check the URL and try again.")
            title = clean_filename(info.get('title', 'unknown_title'))
            print(f" Job {job_id} - downloading: {title}")

            ydl.download([url])
        
        job_store[job_id]['status'] = 'completed'
        job_store[job_id]['title'] = title
        job_store[job_id]['filename'] = f"{title}.mp4" if quality!= "audio" else f"{title}.mp3"

        print(f"Job {job_id} completed successfully: {title}")

    except Exception as e:
        job_store[job_id]['status'] = 'error'
        job_store[job_id]['error'] = str(e)
        print(f"Job {job_id} failed with error: {str(e)}")

