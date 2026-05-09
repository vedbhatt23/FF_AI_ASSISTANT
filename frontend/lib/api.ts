import { ChatResponse, HealthStatus } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "dev-api-key-change-me";

const headers = {
  "Content-Type": "application/json",
  "X-API-Key": API_KEY,
};

export async function sendMessage(
  message: string,
  conversationId?: string,
  filters?: Record<string, unknown>
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      filters: filters || null,
    }),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API Error ${res.status}: ${error}`);
  }

  return res.json();
}

export async function checkHealth(): Promise<HealthStatus> {
  const res = await fetch(`${API_BASE}/api/health`, { headers: { "X-API-Key": API_KEY } });
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function triggerIngest(): Promise<unknown> {
  const res = await fetch(`${API_BASE}/api/ingest`, {
    method: "POST",
    headers,
  });
  return res.json();
}
