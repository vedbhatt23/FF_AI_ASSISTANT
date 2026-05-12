"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Sparkles, Loader2, TrendingUp, FileBarChart, Presentation, HelpCircle, PlaySquare } from "lucide-react";
import MessageBubble from "./MessageBubble";
import { useChat } from "../hooks/useChat";

interface Props {
  chatHook: ReturnType<typeof useChat>;
}

const SUGGESTIONS = [
  { text: "Which titles performed best in 2025?", icon: <TrendingUp size={15} /> },
  { text: "Why is Stellar Run trending recently?", icon: <Sparkles size={15} /> },
  { text: "Compare Dark Orbit vs Last Kingdom", icon: <FileBarChart size={15} /> },
  { text: "Which city had strongest engagement?", icon: <Presentation size={15} /> },
  { text: "What explains weak comedy performance?", icon: <HelpCircle size={15} /> },
  { text: "What recommendations would you give?", icon: <PlaySquare size={15} /> },
];

export default function ChatInterface({ chatHook }: Props) {
  const { messages, isLoading, sendMessage, error } = chatHook;
  const [input, setInput] = useState("");
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTo({
        top: scrollContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isLoading]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        flex: 1,
        background: "rgba(15, 23, 42, 0.5)",
        borderRadius: "16px",
        border: "1px solid rgba(99, 102, 241, 0.12)",
        overflow: "hidden",
        height: "100%",
        maxHeight: "100%",
      }}
    >
      {/* Scrollable Messages Area */}
      <div
        ref={scrollContainerRef}
        style={{
          flex: "1 1 0%",
          minHeight: 0,
          overflowY: "auto",
          padding: "24px",
          paddingBottom: "16px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {messages.length === 0 ? (
          /* ── Welcome Screen ── */
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              textAlign: "center",
              maxWidth: "560px",
              margin: "0 auto",
            }}
          >
            <div
              style={{
                width: "64px",
                height: "64px",
                borderRadius: "16px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15))",
                marginBottom: "24px",
              }}
            >
              <Sparkles size={30} color="#3b82f6" />
            </div>

            <h2 style={{ fontSize: "26px", fontWeight: 700, color: "#f1f5f9", marginBottom: "10px" }}>
              Welcome to AI Insights
            </h2>
            <p style={{ fontSize: "14px", color: "#94a3b8", marginBottom: "36px", lineHeight: 1.6, maxWidth: "420px" }}>
              Ask questions about movie performance, viewer demographics, marketing ROI, or internal strategy documents.
            </p>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "12px",
                width: "100%",
              }}
            >
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(s.text)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    padding: "14px 16px",
                    borderRadius: "12px",
                    textAlign: "left",
                    fontSize: "13px",
                    color: "#cbd5e1",
                    background: "rgba(30, 41, 59, 0.5)",
                    border: "1px solid rgba(99, 102, 241, 0.12)",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                    lineHeight: 1.4,
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "rgba(30, 41, 59, 0.8)";
                    e.currentTarget.style.borderColor = "rgba(99, 102, 241, 0.3)";
                    e.currentTarget.style.color = "#f1f5f9";
                    e.currentTarget.style.transform = "translateY(-2px)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "rgba(30, 41, 59, 0.5)";
                    e.currentTarget.style.borderColor = "rgba(99, 102, 241, 0.12)";
                    e.currentTarget.style.color = "#cbd5e1";
                    e.currentTarget.style.transform = "translateY(0)";
                  }}
                >
                  <span style={{ color: "#60a5fa", flexShrink: 0 }}>{s.icon}</span>
                  <span>{s.text}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          /* ── Message Thread ── */
          <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}

            {isLoading && (
              <div style={{ display: "flex", gap: "12px" }} className="animate-fade-in-up">
                <div
                  style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "8px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background: "rgba(30, 41, 59, 0.8)",
                    border: "1px solid rgba(99, 102, 241, 0.15)",
                    flexShrink: 0,
                  }}
                >
                  <Sparkles size={16} color="#3b82f6" style={{ opacity: 0.6 }} />
                </div>
                <div
                  style={{
                    display: "flex",
                    gap: "4px",
                    alignItems: "center",
                    padding: "10px 20px",
                    background: "rgba(30, 41, 59, 0.5)",
                    border: "1px solid rgba(99, 102, 241, 0.12)",
                    borderRadius: "16px",
                    borderTopLeftRadius: "4px",
                  }}
                >
                  <div className="typing-dot" style={{ width: "6px", height: "6px", background: "#3b82f6", borderRadius: "50%" }} />
                  <div className="typing-dot" style={{ width: "6px", height: "6px", background: "#3b82f6", borderRadius: "50%" }} />
                  <div className="typing-dot" style={{ width: "6px", height: "6px", background: "#3b82f6", borderRadius: "50%" }} />
                </div>
              </div>
            )}

            {error && (
              <div
                style={{
                  padding: "12px",
                  background: "rgba(127, 29, 29, 0.2)",
                  border: "1px solid rgba(127, 29, 29, 0.5)",
                  borderRadius: "12px",
                  fontSize: "12px",
                  color: "#fca5a5",
                  textAlign: "center",
                }}
              >
                {error}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Fixed Input Bar ── */}
      <div
        style={{
          flexShrink: 0,
          padding: "16px 20px 20px 20px",
          borderTop: "1px solid rgba(99, 102, 241, 0.1)",
          background: "rgba(15, 23, 42, 0.5)",
        }}
      >
        <form onSubmit={handleSubmit}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              background: "rgba(15, 23, 42, 0.8)",
              borderRadius: "12px",
              border: "1px solid rgba(99, 102, 241, 0.15)",
              padding: "4px 4px 4px 16px",
            }}
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about the entertainment data..."
              style={{
                flex: 1,
                background: "transparent",
                border: "none",
                outline: "none",
                fontSize: "14px",
                color: "#f1f5f9",
                padding: "10px 0",
              }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              style={{
                width: "40px",
                height: "40px",
                borderRadius: "10px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
                border: "none",
                cursor: input.trim() && !isLoading ? "pointer" : "not-allowed",
                opacity: input.trim() && !isLoading ? 1 : 0.4,
                background: input.trim() && !isLoading ? "linear-gradient(135deg, #3b82f6, #8b5cf6)" : "rgba(255,255,255,0.05)",
                transition: "all 0.2s",
              }}
            >
              {isLoading ? (
                <Loader2 size={18} color="#94a3b8" className="animate-spin" />
              ) : (
                <Send size={16} color={input.trim() ? "white" : "#64748b"} />
              )}
            </button>
          </div>
        </form>
        <p style={{ textAlign: "center", marginTop: "8px", fontSize: "10px", color: "#475569" }}>
          AI responses are generated based on internal structured & unstructured data sources.
        </p>
      </div>
    </div>
  );
}
