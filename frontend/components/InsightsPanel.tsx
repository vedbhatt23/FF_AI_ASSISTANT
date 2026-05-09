"use client";

import { ToolExecution } from "../lib/types";
import { Activity, Database, FileText, ChevronDown, ChevronRight, Clock, Box } from "lucide-react";
import { useState } from "react";

interface Props {
  history: ToolExecution[];
}

function TraceItem({ trace, index }: { trace: ToolExecution; index: number }) {
  const [expanded, setExpanded] = useState(index === 0); // Expand latest by default
  const isSql = trace.source_type === "sql_database";

  return (
    <div className="mb-4 relative">
      {/* Timeline line connecting items */}
      <div className="absolute left-[15px] top-8 bottom-[-24px] w-0.5 bg-gray-800/50 z-0"></div>

      <div className="relative z-10 flex gap-3">
        {/* Icon */}
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 border mt-0.5"
          style={{
            background: isSql ? "rgba(59, 130, 246, 0.1)" : "rgba(139, 92, 246, 0.1)",
            borderColor: isSql ? "rgba(59, 130, 246, 0.3)" : "rgba(139, 92, 246, 0.3)",
            color: isSql ? "#60a5fa" : "#a78bfa",
          }}
        >
          {isSql ? <Database size={14} /> : <FileText size={14} />}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <button
            onClick={() => setExpanded(!expanded)}
            className="w-full text-left flex items-center justify-between group"
          >
            <div>
              <p className="text-sm font-medium text-gray-200 truncate pr-2 group-hover:text-white transition-colors">
                {trace.tool_name.replace(/_/g, " ")}
              </p>
              <div className="flex items-center gap-3 text-[11px] text-gray-500 mt-0.5">
                <span className="flex items-center gap-1"><Clock size={10} /> {trace.execution_time_ms}ms</span>
                {trace.row_count !== undefined && (
                  <span className="flex items-center gap-1"><Box size={10} /> {trace.row_count} rows</span>
                )}
              </div>
            </div>
            {expanded ? <ChevronDown size={14} className="text-gray-500" /> : <ChevronRight size={14} className="text-gray-500" />}
          </button>

          {/* Details */}
          {expanded && (
            <div className="mt-3 animate-fade-in space-y-3">
              {/* Arguments */}
              {Object.keys(trace.arguments).length > 0 && (
                <div className="bg-black/30 rounded-lg p-2.5 border border-gray-800/50">
                  <p className="text-[10px] uppercase text-gray-500 mb-1 font-semibold tracking-wider">Parameters</p>
                  <pre className="text-xs text-gray-300 font-mono overflow-x-auto whitespace-pre-wrap">
                    {JSON.stringify(trace.arguments, null, 2)}
                  </pre>
                </div>
              )}

              {/* Result Summary */}
              <div className="bg-blue-900/10 rounded-lg p-2.5 border border-blue-900/20">
                <p className="text-[10px] uppercase text-blue-400 mb-1 font-semibold tracking-wider">Result</p>
                <p className="text-xs text-gray-300 leading-relaxed">
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
      <div className="h-full flex flex-col items-center justify-center text-center p-6 bg-slate-900/40 rounded-2xl border border-dashed border-gray-800/50 shadow-lg">
        <div className="w-16 h-16 rounded-full bg-gray-800/50 flex items-center justify-center mb-4 text-gray-500">
          <Activity size={24} />
        </div>
        <h2 className="text-gray-300 font-medium mb-2">No active trace</h2>
        <p className="text-sm text-gray-500">
          As you ask questions, this panel will reveal exactly which databases, documents, and tools the AI is accessing.
        </p>
      </div>
    );
  }

  // Reverse to show newest at top
  const reversedHistory = [...history].reverse();

  return (
    <div className="h-full flex flex-col bg-slate-900/40 rounded-2xl border border-gray-800/50 overflow-hidden relative shadow-lg">
      <div className="p-4 border-b border-gray-800/50 flex items-center justify-between bg-black/20">
        <div className="flex items-center gap-2">
          <Activity size={16} className="text-blue-400" />
          <h2 className="font-semibold text-sm text-gray-200">Execution Trace</h2>
        </div>
        <div className="px-2 py-0.5 rounded-full bg-gray-800/80 text-[10px] font-medium text-gray-400">
          {history.length} {history.length === 1 ? 'step' : 'steps'}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-5 custom-scrollbar">
        {reversedHistory.map((trace, i) => (
          <TraceItem key={i} trace={trace} index={i} />
        ))}
      </div>
    </div>
  );
}
