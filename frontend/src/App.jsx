import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I am EduBot 👋 I can answer questions about ICT Academy of Kerala. Ask me about courses, admissions, fees, or contact details!",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question: input,
      });
      const botMessage = { role: "bot", text: res.data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  const quickReplies = [
    "What courses are available?",
    "Is there a scholarship?",
    "Where is ICTAK located?",
    "Who is the CEO?",
    "How to apply?",
  ];

  return (
    <div className="app">
      {/* Header */}
      <div className="header">
        <div className="header-avatar">🎓</div>
        <div>
          <div className="header-title">EduBot</div>
          <div className="header-subtitle">ICT Academy of Kerala</div>
        </div>
        <div className="header-status">● Online</div>
      </div>

      {/* Messages */}
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === "bot" && <div className="avatar">🤖</div>}
            <div className="bubble">{msg.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="avatar">🤖</div>
            <div className="bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick replies */}
      <div className="quick-replies">
        {quickReplies.map((q, i) => (
          <button key={i} onClick={() => { setInput(q); }}>
            {q}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="input-area">
        <input
          type="text"
          placeholder="Ask me anything about ICTAK..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
