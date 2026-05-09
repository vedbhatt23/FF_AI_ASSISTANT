"use client";

import { useState, useCallback } from "react";
import { Message, ToolExecution } from "../lib/types";
import { sendMessage as apiSendMessage } from "../lib/api";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [toolHistory, setToolHistory] = useState<ToolExecution[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string, filters?: Record<string, unknown>) => {
      setError(null);
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: "user",
        content,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response = await apiSendMessage(content, conversationId, filters);

        setConversationId(response.conversation_id);

        const assistantMessage: Message = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          chart_data: response.chart_data,
          timestamp: response.timestamp,
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setToolHistory((prev) => [...prev, ...response.sources]);
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Unknown error";
        setError(msg);
        const errorMessage: Message = {
          id: `error-${Date.now()}`,
          role: "assistant",
          content: `Sorry, I encountered an error: ${msg}`,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setConversationId(undefined);
    setToolHistory([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    conversationId,
    toolHistory,
    error,
    sendMessage,
    clearChat,
  };
}
