"use client";

import Header from "../components/Header";
import ChatInterface from "../components/ChatInterface";
import InsightsPanel from "../components/InsightsPanel";
import { useChat } from "../hooks/useChat";
import { useEffect, useState } from "react";

export default function Home() {
  const chatHook = useChat();
  const [mounted, setMounted] = useState(false);

  // Avoid hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="h-screen flex flex-col bg-slate-950 relative overflow-hidden">
      {/* Background ambient light */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Header */}
      <Header onClear={chatHook.clearChat} messageCount={chatHook.messages.length} />

      {/* Main Layout: Chat + Insights Panel */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden pb-4 px-4 gap-4">
        {/* Left Column: Chat */}
        <div className="flex-1 min-w-0 h-full overflow-hidden">
          <ChatInterface chatHook={chatHook} />
        </div>

        {/* Right Column: Insights/Trace Panel */}
        <div className="w-full lg:w-[400px] xl:w-[450px] shrink-0 h-[40vh] lg:h-full overflow-hidden">
          <InsightsPanel history={chatHook.toolHistory} />
        </div>
      </div>
    </div>
  );
}
