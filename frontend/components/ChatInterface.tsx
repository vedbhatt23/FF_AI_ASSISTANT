"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Sparkles, Loader2, PlaySquare, FileBarChart, Presentation, TrendingUp, HelpCircle } from "lucide-react";
import MessageBubble from "./MessageBubble";
import FilterBar from "./FilterBar";
import { useChat } from "../hooks/useChat";

interface Props {
  chatHook: ReturnType<typeof useChat>;
}

const SUGGESTIONS = [
  { text: "Which titles performed best in 2025?", icon: <TrendingUp size={14} /> },
  { text: "Why is Stellar Run trending recently?", icon: <Sparkles size={14} /> },
  { text: "Compare Dark Orbit vs Last Kingdom", icon: <FileBarChart size={14} /> },
  { text: "Which city had strongest engagement?", icon: <Presentation size={14} /> },
  { text: "What explains weak comedy performance?", icon: <HelpCircle size={14} /> },
  { text: "What recommendations would you give?", icon: <PlaySquare size={14} /> },
];

export default function ChatInterface({ chatHook }: Props) {
  const { messages, isLoading, sendMessage, error } = chatHook;
  const [input, setInput] = useState("");
  const [filters, setFilters] = useState<Record<string, any> | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input, filters);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-900/40 rounded-2xl border border-gray-800/50 overflow-hidden relative shadow-lg">
      {/* Messages Area */}
      <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-6 pb-6 pt-2 relative">
        <FilterBar onFilterChange={setFilters} />

        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center max-w-xl mx-auto text-center animate-fade-in-up">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-6" style={{ background: "var(--gradient-card)" }}>
              <Sparkles size={32} style={{ color: "var(--accent-blue)" }} />
            </div>
            <h2 className="text-2xl font-semibold mb-3">Welcome to AI Insights</h2>
            <p className="text-sm text-gray-400 mb-8 max-w-md">
              Ask questions about movie performance, viewer demographics, marketing ROI, or internal strategy documents.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(s.text, filters)}
                  className="flex items-center gap-3 p-3 rounded-xl text-left text-sm transition-all duration-200 hover:-translate-y-1 group"
                  style={{ background: "rgba(30, 41, 59, 0.4)", border: "1px solid var(--border-glass)" }}
                >
                  <div className="text-blue-400 group-hover:text-blue-300 transition-colors">{s.icon}</div>
                  <span className="text-gray-300 group-hover:text-white transition-colors">{s.text}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-6 pt-4">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            
            {isLoading && (
              <div className="flex gap-3 animate-fade-in-up">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border border-gray-800 bg-gray-900/80">
                  <Sparkles size={16} className="text-blue-500 opacity-50" />
                </div>
                <div className="glass-card px-5 py-4 rounded-2xl rounded-tl-sm flex gap-1 items-center h-10">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full typing-dot"></div>
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full typing-dot"></div>
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full typing-dot"></div>
                </div>
              </div>
            )}
            
            {error && (
               <div className="p-3 bg-red-900/20 border border-red-900/50 rounded-xl text-xs text-red-400 text-center animate-fade-in">
                 {error}
               </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="shrink-0 p-4 pt-2 z-20 bg-[#0a0e1a] border-t border-gray-800/50 relative">
        <form onSubmit={handleSubmit} className="relative group">
          <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 opacity-20 blur group-focus-within:opacity-40 transition-opacity"></div>
          <div className="relative flex items-end gap-2 bg-gray-900/90 rounded-xl border border-gray-700/50 p-2 focus-within:border-gray-500/50 transition-colors">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about the entertainment data..."
              className="flex-1 max-h-32 min-h-[44px] bg-transparent border-none outline-none resize-none px-3 py-2.5 text-sm text-gray-100 placeholder-gray-500"
              rows={1}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="w-11 h-11 rounded-lg flex items-center justify-center shrink-0 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ background: input.trim() && !isLoading ? "var(--gradient-primary)" : "rgba(255,255,255,0.05)" }}
            >
              {isLoading ? (
                <Loader2 size={18} className="animate-spin text-gray-400" />
              ) : (
                <Send size={18} className={input.trim() ? "text-white ml-1" : "text-gray-500"} />
              )}
            </button>
          </div>
        </form>
        <div className="text-center mt-2">
          <span className="text-[10px] text-gray-600">AI responses are generated based on internal structured & unstructured data sources.</span>
        </div>
      </div>
    </div>
  );
}
