import { useState } from "react";
import type { KeyboardEvent } from "react";

interface Props {
  onSend: (text: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("");

  function submit() {
    if (!text.trim() || disabled) return;
    onSend(text);
    setText("");
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <div className="input-row">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="Ask about your calendar, email or GitHub..."
        maxLength={2000}
        rows={2}
      />
      <button onClick={submit} disabled={disabled || !text.trim()}>
        Send
      </button>
    </div>
  );
}