"use client";

import { ChartData } from "../lib/types";
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

interface Props {
  chartData: ChartData;
}

const DEFAULT_COLORS = [
  "#3b82f6", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b",
  "#f43f5e", "#ec4899", "#14b8a6",
];

const tooltipStyle = {
  backgroundColor: "rgba(17, 24, 39, 0.95)",
  border: "1px solid rgba(99, 102, 241, 0.3)",
  borderRadius: "10px",
  color: "#f1f5f9",
  fontSize: "12px",
  padding: "8px 12px",
};

export default function ChartRenderer({ chartData }: Props) {
  const { chart_type, title, data, x_key, y_keys, colors } = chartData;
  const palette = colors || DEFAULT_COLORS;

  if (!data || data.length === 0) return null;

  const renderChart = () => {
    switch (chart_type) {
      case "bar":
        return (
          <BarChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey={x_key} tick={{ fill: "#94a3b8", fontSize: 11 }} angle={-20} textAnchor="end" height={60} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }} />
            {y_keys.map((key, i) => (
              <Bar key={key} dataKey={key} fill={palette[i % palette.length]}
                radius={[4, 4, 0, 0]} animationDuration={800} />
            ))}
          </BarChart>
        );

      case "line":
        return (
          <LineChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey={x_key} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ fontSize: "12px" }} />
            {y_keys.map((key, i) => (
              <Line key={key} type="monotone" dataKey={key} stroke={palette[i % palette.length]}
                strokeWidth={2} dot={{ r: 4, fill: palette[i % palette.length] }}
                animationDuration={800} />
            ))}
          </LineChart>
        );

      case "pie":
        return (
          <PieChart>
            <Pie data={data} dataKey={y_keys[0]} nameKey={x_key}
              cx="50%" cy="50%" outerRadius={100} innerRadius={40}
              paddingAngle={3} animationDuration={800} label>
              {data.map((_, i) => (
                <Cell key={i} fill={palette[i % palette.length]} />
              ))}
            </Pie>
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ fontSize: "12px" }} />
          </PieChart>
        );

      case "area":
        return (
          <AreaChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey={x_key} tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ fontSize: "12px" }} />
            {y_keys.map((key, i) => (
              <Area key={key} type="monotone" dataKey={key} fill={palette[i % palette.length]}
                fillOpacity={0.15} stroke={palette[i % palette.length]}
                strokeWidth={2} animationDuration={800} />
            ))}
          </AreaChart>
        );

      default:
        return <p className="text-sm" style={{ color: "var(--text-muted)" }}>Unsupported chart type</p>;
    }
  };

  return (
    <div className="mt-4 animate-fade-in-up">
      <p className="text-sm font-medium mb-3" style={{ color: "var(--text-secondary)" }}>
        {title}
      </p>
      <div className="glass-card p-4 rounded-xl" style={{ background: "rgba(15, 23, 42, 0.6)" }}>
        <ResponsiveContainer width="100%" height={280}>
          {renderChart()}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
