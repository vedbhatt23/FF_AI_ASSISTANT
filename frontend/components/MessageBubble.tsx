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
    <div className={`flex gap-3 animate-fade-in-up ${isUser ? "flex-row-reverse" : ""}`}>
      {/* Avatar */}
      <div
        className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-1"
        style={{
          background: isUser ? "var(--gradient-primary)" : "rgba(30, 41, 59, 0.8)",
          border: isUser ? "none" : "1px solid var(--border-glass)",
        }}
      >
        {isUser ? <User size={16} className="text-white" /> : <Bot size={16} style={{ color: "var(--accent-blue)" }} />}
      </div>

      {/* Content */}
      <div className={`max-w-[85%] ${isUser ? "items-end" : "items-start"}`}>
        <div
          className="rounded-2xl px-4 py-3"
          style={{
            background: isUser
              ? "var(--gradient-primary)"
              : "var(--bg-glass)",
            border: isUser ? "none" : "1px solid var(--border-glass)",
            backdropFilter: isUser ? "none" : "blur(20px)",
            borderTopRightRadius: isUser ? "4px" : "16px",
            borderTopLeftRadius: isUser ? "16px" : "4px",
          }}
        >
          {isUser ? (
            <p className="text-sm text-white leading-relaxed">{message.content}</p>
          ) : (
            <div className="prose-chat text-sm overflow-x-auto max-w-full" style={{ color: "var(--text-primary)" }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Chart */}
        {message.chart_data && <ChartRenderer chartData={message.chart_data} />}

        {/* Source badges */}
        {message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-2 animate-fade-in">
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
        <p className="text-[10px] mt-1 px-1" style={{ color: "var(--text-muted)" }}>
          {new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>
    </div>
  );
}
