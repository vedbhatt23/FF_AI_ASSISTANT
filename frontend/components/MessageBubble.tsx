"use client";

import { Message } from "../lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ChartRenderer from "./ChartRenderer";
import { Database, FileText, Bot, User } from "lucide-react";

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      className="animate-fade-in-up"
      style={{
        display: "flex",
        gap: "12px",
        flexDirection: isUser ? "row-reverse" : "row",
      }}
    >
      {/* Avatar */}
      <div
        style={{
          width: "32px",
          height: "32px",
          borderRadius: "8px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
          marginTop: "4px",
          background: isUser ? "linear-gradient(135deg, #3b82f6, #8b5cf6)" : "rgba(30, 41, 59, 0.8)",
          border: isUser ? "none" : "1px solid rgba(99, 102, 241, 0.15)",
        }}
      >
        {isUser ? <User size={16} color="white" /> : <Bot size={16} color="#3b82f6" />}
      </div>

      {/* Content */}
      <div style={{ maxWidth: "80%" }}>
        <div
          style={{
            borderRadius: "16px",
            padding: "14px 18px",
            background: isUser
              ? "linear-gradient(135deg, #3b82f6, #8b5cf6)"
              : "rgba(30, 41, 59, 0.5)",
            border: isUser ? "none" : "1px solid rgba(99, 102, 241, 0.12)",
            borderTopRightRadius: isUser ? "4px" : "16px",
            borderTopLeftRadius: isUser ? "16px" : "4px",
          }}
        >
          {isUser ? (
            <p style={{ fontSize: "14px", color: "white", lineHeight: 1.6, margin: 0 }}>{message.content}</p>
          ) : (
            <div className="prose-chat" style={{ fontSize: "14px", color: "#e2e8f0", overflowX: "auto" }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Chart */}
        {message.chart_data && (
          <div style={{ marginTop: "12px" }}>
            <ChartRenderer chartData={message.chart_data} />
          </div>
        )}

        {/* Source badges */}
        {message.sources && message.sources.length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "8px" }}>
            {message.sources.map((s, i) => (
              <span
                key={i}
                className={`source-badge ${s.source_type === "sql_database" ? "sql" : "vector"}`}
              >
                {s.source_type === "sql_database" ? <Database size={10} /> : <FileText size={10} />}
                {s.tool_name.replace(/_/g, " ")}
                <span style={{ opacity: 0.6 }}>{s.execution_time_ms}ms</span>
              </span>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <p style={{ fontSize: "10px", color: "#64748b", marginTop: "4px", paddingLeft: "4px" }}>
          {new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>
    </div>
  );
}
