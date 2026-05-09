"use client";

import { ToolExecution } from "../lib/types";
import { Activity, Database, FileText, ChevronDown, ChevronRight, Clock, Box } from "lucide-react";
import { useState } from "react";

interface Props {
  history: ToolExecution[];
}

function TraceItem({ trace, index }: { trace: ToolExecution; index: number }) {
  const [expanded, setExpanded] = useState(index === 0);
  const isSql = trace.source_type === "sql_database";

  return (
    <div style={{ marginBottom: "16px", position: "relative" }}>
      <div style={{ display: "flex", gap: "12px", position: "relative", zIndex: 1 }}>
        {/* Icon */}
        <div
          style={{
            width: "32px",
            height: "32px",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            background: isSql ? "rgba(59, 130, 246, 0.1)" : "rgba(139, 92, 246, 0.1)",
            border: `1px solid ${isSql ? "rgba(59, 130, 246, 0.3)" : "rgba(139, 92, 246, 0.3)"}`,
            color: isSql ? "#60a5fa" : "#a78bfa",
          }}
        >
          {isSql ? <Database size={14} /> : <FileText size={14} />}
        </div>

        {/* Content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <button
            onClick={() => setExpanded(!expanded)}
            style={{
              width: "100%",
              textAlign: "left",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: 0,
            }}
          >
            <div>
              <p style={{ fontSize: "13px", fontWeight: 500, color: "#e2e8f0", margin: 0 }}>
                {trace.tool_name.replace(/_/g, " ")}
              </p>
              <div style={{ display: "flex", alignItems: "center", gap: "12px", marginTop: "3px" }}>
                <span style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "#64748b" }}>
                  <Clock size={10} /> {trace.execution_time_ms}ms
                </span>
                {trace.row_count !== undefined && (
                  <span style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "#64748b" }}>
                    <Box size={10} /> {trace.row_count} rows
                  </span>
                )}
              </div>
            </div>
            {expanded ? <ChevronDown size={14} color="#64748b" /> : <ChevronRight size={14} color="#64748b" />}
          </button>

          {expanded && (
            <div className="animate-fade-in" style={{ marginTop: "12px", display: "flex", flexDirection: "column", gap: "10px" }}>
              {Object.keys(trace.arguments).length > 0 && (
                <div style={{ background: "rgba(0,0,0,0.3)", borderRadius: "8px", padding: "10px", border: "1px solid rgba(255,255,255,0.05)" }}>
                  <p style={{ fontSize: "10px", textTransform: "uppercase", color: "#64748b", marginBottom: "6px", fontWeight: 600, letterSpacing: "0.05em" }}>
                    Parameters
                  </p>
                  <pre style={{ fontSize: "12px", color: "#cbd5e1", fontFamily: "monospace", overflowX: "auto", whiteSpace: "pre-wrap", margin: 0, wordBreak: "break-word" }}>
                    {JSON.stringify(trace.arguments, null, 2)}
                  </pre>
                </div>
              )}

              <div style={{ background: "rgba(59, 130, 246, 0.05)", borderRadius: "8px", padding: "10px", border: "1px solid rgba(59, 130, 246, 0.1)" }}>
                <p style={{ fontSize: "10px", textTransform: "uppercase", color: "#60a5fa", marginBottom: "6px", fontWeight: 600, letterSpacing: "0.05em" }}>
                  Result
                </p>
                <p style={{ fontSize: "12px", color: "#cbd5e1", lineHeight: 1.5, margin: 0, wordBreak: "break-word" }}>
                  {trace.result_summary}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function InsightsPanel({ history }: Props) {
  if (!history || history.length === 0) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          padding: "32px",
          background: "rgba(15, 23, 42, 0.4)",
          borderRadius: "16px",
          border: "1px dashed rgba(99, 102, 241, 0.2)",
        }}
      >
        <div
          style={{
            width: "56px",
            height: "56px",
            borderRadius: "50%",
            background: "rgba(30, 41, 59, 0.6)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginBottom: "16px",
            color: "#64748b",
          }}
        >
          <Activity size={24} />
        </div>
        <h2 style={{ fontSize: "15px", fontWeight: 600, color: "#cbd5e1", marginBottom: "8px" }}>
          Execution Trace
        </h2>
        <p style={{ fontSize: "13px", color: "#64748b", lineHeight: 1.6, maxWidth: "240px" }}>
          As you ask questions, this panel will show exactly which tools and databases the AI accesses.
        </p>
      </div>
    );
  }

  const reversedHistory = [...history].reverse();

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: "rgba(15, 23, 42, 0.5)",
        borderRadius: "16px",
        border: "1px solid rgba(99, 102, 241, 0.12)",
        overflow: "hidden",
      }}
    >
      {/* Panel Header */}
      <div
        style={{
          padding: "14px 16px",
          borderBottom: "1px solid rgba(99, 102, 241, 0.1)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "rgba(0, 0, 0, 0.2)",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <Activity size={16} color="#60a5fa" />
          <h2 style={{ fontSize: "14px", fontWeight: 600, color: "#e2e8f0", margin: 0 }}>Execution Trace</h2>
        </div>
        <div
          style={{
            padding: "2px 10px",
            borderRadius: "9999px",
            background: "rgba(30, 41, 59, 0.8)",
            fontSize: "11px",
            fontWeight: 500,
            color: "#94a3b8",
          }}
        >
          {history.length} {history.length === 1 ? "step" : "steps"}
        </div>
      </div>

      {/* Trace Items */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", minHeight: 0 }}>
        {reversedHistory.map((trace, i) => (
          <TraceItem key={i} trace={trace} index={i} />
        ))}
      </div>
    </div>
  );
}
