const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

export async function getHealth(): Promise<{ status: string; environment: string }> {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}