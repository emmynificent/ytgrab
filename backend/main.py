from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid 
from tasks import run_download, parse_time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


job_store = {}

class DownloadRequest(BaseModel):
    url : str
    quality: str = "best"
    is_playlist :bool =  False
    starttime: str | None = None
    endtime: str | None = None

@app.get("/")
def root():
    return {"message": "YT Downloader API is running"}

@app.post("/download")
def start_download(request: DownloadRequest, background_task: BackgroundTasks):
    # Treat empty strings the same as None
    starttime = request.starttime or None
    endtime = request.endtime or None

    valid_qualities = ["best", "1080", "720", "audio"]
    if request.quality not in valid_qualities:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid quality. Choose from: {valid_qualities}"
        )

    if starttime or endtime:
        if not starttime or not endtime:
            raise HTTPException(
                status_code=400,
                detail="Both starttime and endtime are required for trimming"
            )
        if not parse_time(starttime) or not parse_time(endtime):
            raise HTTPException(
                status_code=400,
                detail="Invalid time format. Use HH:MM:SS, MM:SS, or plain seconds"
            )

    job_id = str(uuid.uuid4())
    job_store[job_id] = {
        "status": "queued",
        "progress": {},
        "title": None,
        "filename": None,
        "error": None,
    }

    background_task.add_task(
        run_download,
        job_id,
        job_store,
        request.url,
        request.quality,
        request.is_playlist,
        starttime,  # cleaned value
        endtime     # cleaned value
    )

    return {
        "job_id": job_id,
        "message": "Download started",
    }


@app.get("/status/{job_id}")

def get_status(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_store[job_id]

@app.get("/download/{job_id}")
def get_download(job_id: str):
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    job = job_store[job_id]
    if job["status"] != "done":
        raise HTTPException(status_code=400, detail="Download not ready")
    file_path = os.path.join("downloads", job["filename"])

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path = file_path,
        filename= job["filename"],
        media_type="application/octet-stream"
    )