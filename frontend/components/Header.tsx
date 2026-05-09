"use client";

import { useState, useEffect } from "react";
import { Activity, Sparkles, Trash2 } from "lucide-react";
import { checkHealth } from "../lib/api";

interface HeaderProps {
  onClear: () => void;
  messageCount: number;
}

export default function Header({ onClear, messageCount }: HeaderProps) {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const check = async () => {
      try {
        const h = await checkHealth();
        setIsHealthy(h.status === "healthy");
      } catch {
        setIsHealthy(false);
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "14px 24px",
        margin: "16px 16px 0 16px",
        background: "rgba(30, 41, 59, 0.5)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(99, 102, 241, 0.15)",
        borderRadius: "16px",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <div
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "12px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
          }}
        >
          <Sparkles size={20} color="white" />
        </div>
        <div>
          <h1 className="gradient-text" style={{ fontSize: "18px", fontWeight: 600, lineHeight: 1.2 }}>
            AI Insights Assistant
          </h1>
          <p style={{ fontSize: "12px", color: "#64748b", marginTop: "2px" }}>
            Entertainment Analytics Platform
          </p>
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12px", color: "#94a3b8" }}>
          <Activity size={14} />
          <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: isHealthy === null ? "#f59e0b" : isHealthy ? "#10b981" : "#f43f5e",
                boxShadow: isHealthy ? "0 0 8px rgba(16, 185, 129, 0.5)" : "none",
              }}
            />
            {isHealthy === null ? "Connecting..." : isHealthy ? "All Systems Online" : "Degraded"}
          </span>
        </div>

        {messageCount > 0 && (
          <button
            onClick={onClear}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              padding: "6px 12px",
              borderRadius: "8px",
              fontSize: "12px",
              fontWeight: 500,
              background: "rgba(244, 63, 94, 0.1)",
              color: "#f43f5e",
              border: "1px solid rgba(244, 63, 94, 0.2)",
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            <Trash2 size={13} />
            Clear Chat
          </button>
        )}
      </div>
    </header>
  );
}
