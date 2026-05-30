import { useState } from 'react';


const QUALITY_OPTIONS = [
    { label: 'Best', value: 'best' },
    { label: '1080p', value: '1080' },
    { label: '720p', value: '720' },
    { label: 'MP3', value: 'audio' },
];

export default function DownloadForm({ onSubmit, isLoading }) {
    const [url, setUrl] = useState("");
    const [quality, setQuality] = useState("best");
    const [isPlaylist, setIsPlaylist] = useState(false);
    const [trim, setTrim] = useState(false);
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        onSubmit({
            url,  
            quality,
            is_playlist: isPlaylist,
            starttime: trim ? startTime : null,
            endtime: trim ? endTime : null,
        });
    }

    return (
        <form onSubmit={handleSubmit} className="download-form">

            <div className="form-group">
                <span className="form-label">Video URL</span>
                <input
                    type="text"
                    placeholder="https://youtube.com/watch?v=..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    required
                />
            </div>

            <div className="form-group">
                <span className="form-label">Quality</span>
                <div className="quality-pills">
                    {QUALITY_OPTIONS.map((opt) => (
                        <button
                            key={opt.value}
                            type="button"                         
                            className={`quality-pill ${quality === opt.value ? 'active' : ''}`}
                            onClick={() => setQuality(opt.value)}
                        >
                            {opt.label}
                        </button>
                    ))}
                </div>
            </div>

            <div className="toggles-row">

                <label className={`toggle-chip ${isPlaylist ? 'active' : ''}`}>
                    <input
                        type="checkbox"
                        checked={isPlaylist}
                        onChange={(e) => setIsPlaylist(e.target.checked)}
                    />
                    <span className="toggle-dot" />
                    Playlist
                </label>

                
                <label className={`toggle-chip ${trim ? 'active' : ''}`}>
                    <input
                        type="checkbox"
                        checked={trim}
                        onChange={(e) => setTrim(e.target.checked)}
                    />
                    <span className="toggle-dot" />
                    Trim clip
                </label>

            </div>

            {trim && (
                <div className="trim-row">
                    <div className="form-group">
                        <span className="form-label">Start time</span>
                        <input
                            type="text"
                            placeholder="00:01:30"
                            value={startTime}
                            onChange={(e) => setStartTime(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <span className="form-label">End time</span>
                        <input
                            type="text"
                            placeholder="00:03:45"
                            value={endTime}
                            onChange={(e) => setEndTime(e.target.value)}
                            required
                        />
                    </div>
                </div>
            )}

            <button type="submit" className="btn-download" disabled={isLoading}>
                <span className="btn-inner">
                    {isLoading && <span className="spinner" />}
                    {isLoading ? 'Downloading...' : 'Download'}
                </span>
            </button>

        </form>
    );
}