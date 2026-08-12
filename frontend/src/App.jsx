import { useState } from "react";
import "./App.css";

function App() {

  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult("");
    if (url.trim() === "") {
      setError("Masukkan URL terlebih dahulu.");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Terjadi kesalahan.");
      }
      setResult(data.result);
        setHistory(prev => {
      const entry = { url: url, result: data.result };
      const updated = [entry, ...prev.filter(h => h.url !== url)];
      return updated.slice(0, 5);
        });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (

    <div className="app">

      <div className="card">

        <img
          src="/logo.png"
          alt="Logo"
          className="logo"
        />

        <h1 className="title">
          Deteksi URL Phishing
        </h1>

        <p className="subtitle">
          Berbasis Machine Learning 
        </p>
        <div
          className={
            "result-circle" +
            (result !== "" ? " has-result" : "") +
            (result === "Website Phishing" ? " phishing" : "")
          }
        >
          <div className="result-text">

            {result === ""
              ? "Masukkan URL"
              : result}

          </div>

        </div>

        <form
          className="form"
          onSubmit={handleSubmit}
        >

          <input
            type="text"
            className="input-url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button
            className="detect-btn"
            disabled={loading}
          >

            {loading
              ? "Mendeteksi..."
              : "Deteksi"}

          </button>

        </form>

        {loading && (

          <div className="loading">

            <div className="spinner"></div>

            <span>
              Sedang proses deteksi ...
            </span>

          </div>

        )}

        {error && (

          <div className="message error">

            {error}

          </div>

        )}

        {!error && result === "Website Aman" && (

          <div className="message success">

            URL terdeteksi sebagai website yang aman.

          </div>

        )}

        {!error && result === "Website Phishing" && (

          <div className="message error">

            URL terdeteksi sebagai website phishing.

          </div>

        )}
{history.length > 0 && (

  <div className="history">

    <p className="history-label">Riwayat</p>

    <ul className="history-list">

      {history.map((item, idx) => (

        <li
          key={idx}
          className={
            item.result === "Website Phishing"
              ? "history-item phishing"
              : "history-item"
          }
          onClick={() => {
            setUrl(item.url);
            setResult("");
            setError("");
          }}
        >

          <span className="history-badge">
            {item.result === "Website Phishing" ? "PHISHING" : "AMAN"}
          </span>

          <span className="history-url">{item.url}</span>

        </li>

      ))}

    </ul>

  </div>

)}
        <div className="footer">

        </div>

      </div>

    </div>

  );

}

export default App;