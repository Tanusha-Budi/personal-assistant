const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";
const TIMEOUT_MS = 60_000;

export interface ToolCall {
  name: string;
  args: Record<string, unknown>;
}

export interface Usage {
  input_tokens: number;
  output_tokens: number;
}

export interface AgentResponse {
  answer: string;
  tool_calls: ToolCall[];
  usage: Usage;
}

export class ApiError extends Error {
  status: number;
  requestId?: string;

  constructor(message: string, status: number, requestId?: string) {
    super(message);
    this.status = status;
    this.requestId = requestId;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...init,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
  } catch {
    throw new ApiError("Could not reach the server. Is the backend running?", 0);
  }

  const requestId = res.headers.get("X-Request-ID") ?? undefined;

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    let id = requestId;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") message = body.detail;
      if (typeof body.request_id === "string") id = body.request_id;
    } catch {
      // the error body was not JSON, keep the generic message
    }
    throw new ApiError(message, res.status, id);
  }

  return (await res.json()) as T;
}

export function getHealth() {
  return request<{ status: string; environment: string }>("/health");
}

export function runAssistant(message: string) {
  return request<AgentResponse>("/agents/assistant/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}