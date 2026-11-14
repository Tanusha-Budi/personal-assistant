import { useEffect, useState } from "react";
import { getHealth } from "./api/client";

export default function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    getHealth()
      .then((d) => setStatus(`${d.status} (${d.environment})`))
      .catch(() => setStatus("backend unreachable"));
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <h1>Personal Assistant</h1>
      <p>Backend: {status}</p>
    </main>
  );
}