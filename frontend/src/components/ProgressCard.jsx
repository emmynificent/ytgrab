export default function ProgressCard({job, onDownload}){
    if(!job) return null;

    return(
        <div className="progress-card">
            {job.title && <h3>{job.title}</h3>}
            <p className="status">
                Status: <span className={`badge badge -${job.status}`}> {job.status}</span>
             </p>
            {/* {job.status === "running" && job.progress && (
                <div className="progress-details">
                <p>Progress: {job.progress.percent}%</p>
                <p> Speed: {job.progress.speed}</p>
                <p> ETA: {job.progress.eta}</p>
                
                <div className="progress-bar-track">
                    <div className="progress-bar-fill"
                    style={{ width: job.progress.percent}}></div>

                    </div>
                    </div>)} */}
            {job.status === "processing" && (
                <p className="processing-msg"> Post-procesing... almost done</p>
          )}
          {job.status === "done" && (
            <button className="download-btn" onClick={onDownload}>
                Save File
            </button>  
          )}
          {job.status === "error" && (
            <p className="error-msg"> An error occured during download</p>
          )}
        </div>
    );
}