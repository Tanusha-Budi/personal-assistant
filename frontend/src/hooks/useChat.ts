import { useState } from "react";
import { ApiError, runAssistant } from "../api/client";
import type { ToolCall, Usage } from "../api/client";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "error";
  text: string;
  toolCalls?: ToolCall[];
  usage?: Usage;
  requestId?: string;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  async function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role: "user", text: trimmed },
    ]);
    setLoading(true);

    try {
      const res = await runAssistant(trimmed);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: res.answer || "(The assistant returned no answer.)",
          toolCalls: res.tool_calls,
          usage: res.usage,
        },
      ]);
    } catch (e) {
      const err = e instanceof ApiError ? e : null;
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "error",
          text: err?.message ?? "Something went wrong.",
          requestId: err?.requestId,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return { messages, loading, send };
}