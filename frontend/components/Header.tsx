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
    <header className="glass-card flex items-center justify-between px-6 py-4 m-3 mb-0">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center"
          style={{ background: "var(--gradient-primary)" }}>
          <Sparkles size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-lg font-semibold gradient-text">AI Insights Assistant</h1>
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            Entertainment Analytics Platform
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Status */}
        <div className="flex items-center gap-2 text-xs" style={{ color: "var(--text-secondary)" }}>
          <Activity size={14} />
          <span className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 rounded-full"
              style={{
                background: isHealthy === null ? "var(--accent-amber)" : isHealthy ? "var(--accent-emerald)" : "var(--accent-rose)",
                boxShadow: isHealthy ? "0 0 8px rgba(16, 185, 129, 0.5)" : "none",
              }}
            />
            {isHealthy === null ? "Connecting..." : isHealthy ? "All Systems Online" : "Degraded"}
          </span>
        </div>

        {/* Clear */}
        {messageCount > 0 && (
          <button
            onClick={onClear}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 hover:scale-105"
            style={{
              background: "rgba(244, 63, 94, 0.1)",
              color: "var(--accent-rose)",
              border: "1px solid rgba(244, 63, 94, 0.2)",
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
