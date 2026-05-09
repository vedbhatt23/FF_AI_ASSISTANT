export interface ToolExecution {
  tool_name: string;
  arguments: Record<string, unknown>;
  result_summary: string;
  source_type: "sql_database" | "vector_store" | "computed";
  execution_time_ms: number;
  row_count?: number;
}

export interface ChartData {
  chart_type: "bar" | "line" | "pie" | "area";
  title: string;
  data: Record<string, unknown>[];
  x_key: string;
  y_keys: string[];
  colors?: string[];
}

export interface ChatResponse {
  answer: string;
  conversation_id: string;
  sources: ToolExecution[];
  chart_data?: ChartData | null;
  timestamp: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: ToolExecution[];
  chart_data?: ChartData | null;
  timestamp: string;
}

export interface HealthStatus {
  status: string;
  sqlite_status: string;
  sqlite_tables: Record<string, number>;
  chromadb_status: string;
  chromadb_documents: number;
  openai_status: string;
  version: string;
}
