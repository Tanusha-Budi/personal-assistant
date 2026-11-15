import ChatInput from "./components/ChatInput";
import MessageList from "./components/MessageList";
import { useChat } from "./hooks/useChat";
import "./App.css";

export default function App() {
  const { messages, loading, send } = useChat();

  return (
    <div className="app">
      <header>
        <h1>Hazel</h1>
      </header>
      <MessageList messages={messages} loading={loading} />
      <ChatInput onSend={send} disabled={loading} />
    </div>
  );
}