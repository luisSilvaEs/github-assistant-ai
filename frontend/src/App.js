import { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [threadId, setThreadId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/chat", {
        message: input,
        thread_id: threadId,
      });
      setResponse(res.data.response);
      setThreadId(res.data.thread_id); // Preserve thread context
    } catch (error) {
      console.error("API error:", error);
      setResponse("An error occurred. Check console.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "600px" }}>
      <h1>🤖 GitHub Assistant AI</h1>
      <input
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem", marginBottom: "1rem" }}
        type="text"
        placeholder="Type a GitHub command..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSubmit} disabled={loading || !input}>
        {loading ? "Loading..." : "Send"}
      </button>
      {response && (
        <div style={{ marginTop: "2rem", background: "#f6f8fa", padding: "1rem", borderRadius: "5px" }}>
          <strong>Assistant response:</strong>
          <pre>{response}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
