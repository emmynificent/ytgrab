// src/App.jsx
import { useState, useRef } from "react";
import axios from "axios";
import DownloadForm from "./components/DownloadForm";
import ProgressCard from "./components/ProgressCard";
import "./App.css";

const API = "https://ytgrab-a9mt.onrender.com";

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [job,       setJob]       = useState(null);
  const pollRef = useRef(null);

  async function handleSubmit(formData) {
    setIsLoading(true);
    setJob(null);
    try {
      const res = await axios.post(`${API}/download`, formData);
      const { job_id } = res.data;

      // Poll every 2 seconds until the job finishes or errors
      pollRef.current = setInterval(async () => {
        try {
          const statusRes  = await axios.get(`${API}/status/${job_id}`);
          const updatedJob = statusRes.data;
          setJob(updatedJob);

          if (updatedJob.status === "done" || updatedJob.status === "error") {
            clearInterval(pollRef.current);
            setIsLoading(false);
          }
        } catch (err) {
          clearInterval(pollRef.current);
          setIsLoading(false);
          console.error("Status poll failed:", err);
        }
      }, 2000);

    } catch (err) {
      setIsLoading(false);
      const message = err.response?.data?.detail || "Something went wrong.";
      setJob({ status: "error", error: message });
    }
  }

  async function handleDownload() {
    if (!job) return;
    try {
      const res = await axios.get(`${API}/download/${job.job_id}`, {
        responseType: "blob",
      });
      const blobUrl = window.URL.createObjectURL(res.data);
      const link    = document.createElement("a");
      link.href     = blobUrl;
      link.download = job.filename || "download";
      link.click();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error("File download failed:", err);
    }
  }

  return (
    <div className="app">

      {/* ── Header ── */}
      <header className="app-header">
        <div className="app-logo">
          <div className="logo-icon">▶</div>
        </div>
        <h1>YT<span>grab</span></h1>
        <p>Download any YouTube video or audio, fast and free.</p>
      </header>

      {/* ── Main card ── */}
      <div className="card">
        <DownloadForm onSubmit={handleSubmit} isLoading={isLoading} />
      </div>

      {/* ── Progress card — appears after a job starts ── */}
      <ProgressCard job={job} onDownload={handleDownload} />

    </div>
  );
}
