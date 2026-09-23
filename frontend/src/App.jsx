import React, { useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const scanTypes = [
  ["plant", "Plant", "Leaf, stem, whole plant"],
  ["crop", "Crop", "Farm and food crops"],
  ["flower", "Flower", "Garden and ornamental"],
  ["lawn", "Lawn / Grass", "Turf and landscape"],
  ["tree", "Tree / Shrub", "Leaves, bark, fruit"],
];

function App() {
  const [scanType, setScanType] = useState("plant");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const preview = useMemo(() => (file ? URL.createObjectURL(file) : ""), [file]);

  async function analyze() {
    if (!file) return;
    setStatus("loading");
    setError("");
    setResult(null);

    const body = new FormData();
    body.append("image", file);
    body.append("scan_type", scanType);

    try {
      const response = await fetch(`${API_BASE}/scans/analyze/`, {
        method: "POST",
        body,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Analysis request failed.");
      setResult(data);
      setStatus("done");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  }

  return (
    <main className="app-shell">
      <nav className="topbar">
        <div className="brand">
          <div className="brand-mark">PD</div>
          <div>
            <strong>Plant Doctor AR</strong>
            <span>AI plant health diagnostics</span>
          </div>
        </div>
        <div className="nav-status"><i /> Diagnostic workspace</div>
      </nav>

      <section className="hero">
        <div className="eyebrow">VISION-ASSISTED PLANT HEALTH</div>
        <h1>Turn visible plant symptoms into a structured diagnosis.</h1>
        <p>
          Scan crops, flowers, lawns, trees, and garden plants. Plant Doctor AR is being
          built as a professional diagnostic instrument with explainable results.
        </p>
      </section>

      <section className="workspace">
        <div className="panel upload-panel">
          <div className="panel-heading">
            <span>01</span>
            <div><h2>Select scan type</h2><p>Tell the system what kind of vegetation you are inspecting.</p></div>
          </div>

          <div className="type-grid">
            {scanTypes.map(([value, label, detail]) => (
              <button
                key={value}
                className={scanType === value ? "type-card active" : "type-card"}
                onClick={() => setScanType(value)}
              >
                <strong>{label}</strong>
                <small>{detail}</small>
              </button>
            ))}
          </div>

          <div className="panel-heading second">
            <span>02</span>
            <div><h2>Upload image</h2><p>Use a clear photo with the affected area visible.</p></div>
          </div>

          <label className="dropzone">
            {preview ? (
              <img src={preview} alt="Plant preview" />
            ) : (
              <div>
                <div className="scan-ring"><div /></div>
                <strong>Drop or choose a plant image</strong>
                <small>JPG, PNG or WEBP</small>
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              capture="environment"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>

          <button className="analyze-btn" disabled={!file || status === "loading"} onClick={analyze}>
            {status === "loading" ? "Analyzing image..." : "Run diagnostic scan"}
          </button>
          {error && <div className="error-box">{error}</div>}
        </div>

        <aside className="panel diagnosis-panel">
          <div className="diagnostic-header">
            <div><span>LIVE DIAGNOSTIC</span><h2>Analysis output</h2></div>
            <div className="signal"><b />{status === "done" ? "Result ready" : "Awaiting scan"}</div>
          </div>

          {!result ? (
            <div className="empty-result">
              <div className="scanner-visual"><div className="scanner-line" /></div>
              <h3>No diagnosis yet</h3>
              <p>Upload an image and run a scan. The structured diagnosis will appear here.</p>
            </div>
          ) : (
            <div className="result-grid">
              <div className="result-card primary">
                <span>LIKELY CONDITION</span>
                <h3>{result.likely_condition}</h3>
                <p>{result.explanation}</p>
              </div>
              <div className="metric-row">
                <div><span>Plant</span><strong>{result.plant_name}</strong></div>
                <div><span>Confidence</span><strong>{result.confidence}</strong></div>
                <div><span>Severity</span><strong>{result.severity}</strong></div>
              </div>
              <div className="result-card">
                <span>VISIBLE SIGNALS</span>
                <ul>{result.symptoms.map((s) => <li key={s}>{s}</li>)}</ul>
              </div>
              <div className="result-card muted">
                <span>MODEL</span>
                <strong>{result.model_version}</strong>
              </div>
            </div>
          )}
        </aside>
      </section>
    </main>
  );
}

export default App;
