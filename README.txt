# YTGrab

A full-stack YouTube video downloader built with FastAPI and React.

## Features
- Download YouTube videos in best, 1080p, or 720p quality
- Extract audio as MP3
- Trim and download a specific section of a video
- Playlist support
- Live download progress tracking

## Tech Stack
**Backend**
- Python, FastAPI, yt-dlp, FFmpeg

**Frontend**
- React, Vite, Axios

## Running Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then visit `http://localhost:5173`

> **Note:** Requires FFmpeg installed on your machine.
> Download from [ffmpeg.org](https://ffmpeg.org)