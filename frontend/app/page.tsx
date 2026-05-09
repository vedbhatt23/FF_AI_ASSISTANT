"use client";

import Header from "../components/Header";
import ChatInterface from "../components/ChatInterface";
import InsightsPanel from "../components/InsightsPanel";
import { useChat } from "../hooks/useChat";
import { useEffect, useState } from "react";

export default function Home() {
  const chatHook = useChat();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "#0a0e1a",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Background ambient blurs */}
      <div
        style={{
          position: "absolute",
          top: "-20%",
          left: "-10%",
          width: "50%",
          height: "50%",
          background: "rgba(59, 130, 246, 0.06)",
          borderRadius: "50%",
          filter: "blur(120px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-20%",
          right: "-10%",
          width: "50%",
          height: "50%",
          background: "rgba(139, 92, 246, 0.06)",
          borderRadius: "50%",
          filter: "blur(120px)",
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <Header onClear={chatHook.clearChat} messageCount={chatHook.messages.length} />

      {/* Main Content */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "row",
          gap: "16px",
          padding: "16px",
          paddingTop: "8px",
          minHeight: 0,
          overflow: "hidden",
        }}
      >
        {/* Chat Column */}
        <div style={{ flex: 1, minWidth: 0, display: "flex", flexDirection: "column" }}>
          <ChatInterface chatHook={chatHook} />
        </div>

        {/* Insights Panel Column */}
        <div style={{ width: "380px", flexShrink: 0, display: "flex", flexDirection: "column" }}>
          <InsightsPanel history={chatHook.toolHistory} />
        </div>
      </div>
    </div>
  );
}
