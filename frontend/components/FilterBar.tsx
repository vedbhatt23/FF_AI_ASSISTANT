"use client";

import { Filter, X } from "lucide-react";
import { useState } from "react";

interface Props {
  onFilterChange: (filters: Record<string, any> | undefined) => void;
}

const YEARS = [2025, 2024, 2023];
const GENRES = ["Sci-Fi", "Action", "Drama", "Comedy", "Thriller", "Documentary"];

export default function FilterBar({ onFilterChange }: Props) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  const handleApply = () => {
    if (!selectedYear && !selectedGenre) {
      onFilterChange(undefined);
    } else {
      const filters: Record<string, any> = {};
      if (selectedYear) filters.year = selectedYear;
      if (selectedGenre) filters.genre = selectedGenre;
      onFilterChange(filters);
    }
  };

  const handleClear = () => {
    setSelectedYear(null);
    setSelectedGenre(null);
    onFilterChange(undefined);
  };

  const activeCount = (selectedYear ? 1 : 0) + (selectedGenre ? 1 : 0);

  return (
    <div className="relative z-10 px-6 py-2">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-full transition-colors"
        style={{
          background: isOpen || activeCount > 0 ? "rgba(59, 130, 246, 0.15)" : "var(--bg-glass)",
          color: isOpen || activeCount > 0 ? "var(--text-primary)" : "var(--text-secondary)",
          border: `1px solid ${isOpen || activeCount > 0 ? "rgba(59, 130, 246, 0.3)" : "var(--border-glass)"}`,
        }}
      >
        <Filter size={14} />
        {activeCount > 0 ? `Filters (${activeCount})` : "Add Filters"}
      </button>

      {isOpen && (
        <div
          className="absolute top-10 left-6 glass-card p-4 rounded-xl shadow-xl w-72 animate-fade-in-up"
          style={{ border: "1px solid rgba(99, 102, 241, 0.2)" }}
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-sm font-semibold">Context Filters</h3>
            <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white">
              <X size={14} />
            </button>
          </div>

          <div className="space-y-4">
            {/* Year */}
            <div>
              <label className="text-xs text-gray-400 mb-2 block">Release Year</label>
              <div className="flex gap-2">
                {YEARS.map((y) => (
                  <button
                    key={y}
                    onClick={() => setSelectedYear(selectedYear === y ? null : y)}
                    className="text-xs px-3 py-1.5 rounded-md transition-colors"
                    style={{
                      background: selectedYear === y ? "var(--accent-blue)" : "rgba(255,255,255,0.05)",
                      color: selectedYear === y ? "white" : "var(--text-secondary)",
                    }}
                  >
                    {y}
                  </button>
                ))}
              </div>
            </div>

            {/* Genre */}
            <div>
              <label className="text-xs text-gray-400 mb-2 block">Genre</label>
              <div className="flex flex-wrap gap-2">
                {GENRES.map((g) => (
                  <button
                    key={g}
                    onClick={() => setSelectedGenre(selectedGenre === g ? null : g)}
                    className="text-xs px-3 py-1.5 rounded-md transition-colors"
                    style={{
                      background: selectedGenre === g ? "var(--accent-purple)" : "rgba(255,255,255,0.05)",
                      color: selectedGenre === g ? "white" : "var(--text-secondary)",
                    }}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-2 border-t border-gray-800">
              <button
                onClick={handleClear}
                className="flex-1 py-1.5 text-xs text-gray-400 hover:text-white transition-colors rounded-lg bg-gray-800/50"
              >
                Clear
              </button>
              <button
                onClick={() => {
                  handleApply();
                  setIsOpen(false);
                }}
                className="flex-1 py-1.5 text-xs text-white transition-colors rounded-lg"
                style={{ background: "var(--gradient-primary)" }}
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
