import React, { useState } from "react";
import "../assets/market.css";
import { FaSearch } from "react-icons/fa";

const MarketTrends = () => {
  const [query, setQuery] = useState("");
  const [insights, setInsights] = useState("");

  const fetchInsights = () => {
    // Simulating an API response
    const sampleInsights = [
      "Artificial Intelligence is revolutionizing industries.",
      "Blockchain adoption is growing in finance & logistics.",
      "Cloud computing demand continues to rise.",
      "Cybersecurity threats are driving security investments.",
      "Quantum computing is the next frontier for tech."
    ];
    setInsights(sampleInsights);
  };

  return (
    <div className="market-container">
      <h1 className="market-title">📊 Market Trend Forecasting</h1>

      <div className="search-box">
        <FaSearch className="search-icon" />
        <input
          type="text"
          placeholder="Enter your business query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={fetchInsights}>Get Insights</button>
      </div>

      {insights && (
        <div className="results-card">
          <h2>🔍 Insights</h2>
          <ul>
            {insights.map((insight, index) => (
              <li key={index}>{insight}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MarketTrends;
