import { useEffect, useRef } from "react";
import type { ChatMessage } from "../hooks/useChat";

interface Props {
  messages: ChatMessage[];
  loading: boolean;
}

export default function MessageList({ messages, loading }: Props) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="messages">
      {messages.length === 0 && (
        <p className="hint">Try: "What's on my calendar today?"</p>
      )}

      {messages.map((m) => (
        <div key={m.id} className={`bubble ${m.role}`}>
          <div className="text">{m.text}</div>

          {m.toolCalls && m.toolCalls.length > 0 && (
            <details className="meta">
              <summary>
                Used {m.toolCalls.length} tool{m.toolCalls.length > 1 ? "s" : ""}
              </summary>
              <ul>
                {m.toolCalls.map((c, i) => (
                  <li key={i}>
                    <code>{c.name}</code> {JSON.stringify(c.args)}
                  </li>
                ))}
              </ul>
              {m.usage && (
                <p>
                  Tokens: {m.usage.input_tokens} in, {m.usage.output_tokens} out
                </p>
              )}
            </details>
          )}

          {m.requestId && <div className="meta">Request ID: {m.requestId}</div>}
        </div>
      ))}

      {loading && <div className="bubble assistant">Thinking…</div>}
      <div ref={endRef} />
    </div>
  );
}