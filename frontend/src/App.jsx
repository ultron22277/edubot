import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

const SUGGESTIONS = {
  programs: [
    "How much does it cost?",
    "How long is the course?",
    "Is there online option?",
  ],
  admissions: [
    "Is there a scholarship?",
    "What is the registration fee?",
    "When does the batch start?",
  ],
  fees: [
    "Who can apply?",
    "What courses are available?",
    "Where is ICTAK located?",
  ],
  contact: [
    "What courses are available?",
    "How to apply?",
    "Is there a scholarship?",
  ],
  about: [
    "What courses are available?",
    "How to apply?",
    "Where is ICTAK located?",
  ],
  default: [
    "What courses are available?",
    "Is there a scholarship?",
    "Where is ICTAK located?",
    "Who is the CEO?",
    "How to apply?",
  ],
};

function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I am EduBot 👋 I can answer questions about ICT Academy of Kerala. Ask me about courses, admissions, fees, or contact details!",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      intent: "default",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Check backend health
  useEffect(() => {
    const check = async () => {
      try {
        await axios.get("http://127.0.0.1:8000/health");
        setIsOnline(true);
      } catch {
        setIsOnline(false);
      }
    };
    check();
    const interval = setInterval(check, 10000);
    return () => clearInterval(interval);
  }, []);

  const getTime = () =>
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  const sendMessage = async (text) => {
    const question = text || input;
    if (!question.trim()) return;

    const userMessage = { role: "user", text: question, time: getTime() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question,
      });
      const botMessage = {
        role: "bot",
        text: res.data.answer,
        time: getTime(),
        intent: res.data.intent || "default",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Sorry, I am unable to connect right now. Please try again or contact us at +91 75 940 51437.",
          time: getTime(),
          intent: "default",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  const clearChat = () => {
    setMessages([
      {
        role: "bot",
        text: "Hi! I am EduBot 👋 I can answer questions about ICT Academy of Kerala. Ask me about courses, admissions, fees, or contact details!",
        time: getTime(),
        intent: "default",
      },
    ]);
  };

  const quickReplies = [
    "What courses are available?",
    "Is there a scholarship?",
    "Where is ICTAK?",
    "Who is the CEO?",
    "How to apply?",
  ];

  const lastBotMessage = [...messages].reverse().find((m) => m.role === "bot");
  const suggestions = SUGGESTIONS[lastBotMessage?.intent] || SUGGESTIONS.default;

  return (
    <div className="app">
      {/* Header */}
      <div className="header">
        <div className="logo-circle">
          <span>ICT</span>
        </div>
        <div className="header-info">
          <div className="header-title">EduBot</div>
          <div className="header-subtitle">ICT Academy of Kerala</div>
        </div>
        <div className="header-right">
          <div className={`header-status ${isOnline ? "online" : "offline"}`}>
            <span className="dot"></span>
            {isOnline ? "Online" : "Offline"}
          </div>
          <button className="clear-btn" onClick={clearChat} title="Clear chat">
            🗑️
          </button>
        </div>
      </div>

      {/* Subheader */}
      <div className="subheader">
        Ask me anything about ICTAK — courses, admissions, fees &amp; more!
      </div>

      {/* Messages */}
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === "bot" && <div className="avatar">🤖</div>}
            <div className="bubble-wrap">
              <div className="bubble">{msg.text}</div>
              <div className="timestamp">{msg.time}</div>
              {/* Show suggestions after last bot message */}
              {msg.role === "bot" && i === messages.length - 1 && !loading && (
                <div className="suggestions">
                  {suggestions.map((s, j) => (
                    <button key={j} onClick={() => sendMessage(s)}>
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="avatar">🤖</div>
            <div className="bubble-wrap">
              <div className="bubble typing">
                <span></span><span></span><span></span>
              </div>
              <div className="timestamp">typing...</div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick replies */}
      <div className="quick-replies">
        {quickReplies.map((q, i) => (
          <button key={i} onClick={() => sendMessage(q)}>
            {q}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="input-area">
        <input
          type="text"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />
        <button onClick={() => sendMessage()} disabled={loading}>
          {loading ? "..." : "➤"}
        </button>
      </div>

      {/* Footer */}
      <div className="footer">
        Powered by ICT Academy of Kerala &nbsp;|&nbsp; ictkerala.org
      </div>
    </div>
  );
}

export default App;