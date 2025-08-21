"use client";

import { useState } from 'react';

export default function Home() {
  const [ticker, setTicker] = useState('');
  const [period, setPeriod] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleSearch = async () => {
    setLoading(true);
    try {
      // Call API to process earnings call
      const response = await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, period_hint: period }),
      });
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            EarningsCall-TLDR
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            This is not investment advice.
          </p>
        </div>
      </header>

      {/* Search */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Ticker (e.g., AAPL)"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <input
              type="text"
              placeholder="Period (e.g., Q2 FY2025)"
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              onClick={handleSearch}
              disabled={loading || !ticker || !period}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Analyze'}
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {data && (
        <div className="max-w-7xl mx-auto px-4 pb-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              {/* Tier A - Why Stock Moved */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4">Why the Stock Moved</h2>
                <div className="space-y-3">
                  {/* Placeholder for bullets */}
                  <div className="flex items-start gap-3">
                    <span className="text-green-500">↑</span>
                    <div>
                      <p>Revenue beat expectations by 3%</p>
                      <span className="text-sm text-gray-500">Confidence: 85%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Tier B - Plain English Summary */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4">Plain English Summary</h2>
                <p className="text-gray-700 dark:text-gray-300">
                  {data.summary || 'Processing summary...'}
                </p>
              </div>

              {/* Tier C - Expert Analysis */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4">Expert Analysis</h2>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold">Key Metrics</h3>
                    <table className="w-full mt-2">
                      <tbody>
                        <tr>
                          <td className="py-1">Revenue</td>
                          <td className="py-1 text-right">$97.3B (+5% YoY)</td>
                        </tr>
                        <tr>
                          <td className="py-1">EPS</td>
                          <td className="py-1 text-right">$1.53 (+9% YoY)</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column - Price Chart */}
            <div className="lg:col-span-1">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-xl font-bold mb-4">Price Reaction</h2>
                <div className="aspect-square bg-gray-100 rounded flex items-center justify-center">
                  <p className="text-gray-500">Chart placeholder</p>
                </div>
                <div className="mt-4 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>After-hours move:</span>
                    <span className="text-green-500">+2.5%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Next day gap:</span>
                    <span className="text-green-500">+1.8%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Processing earnings call...</p>
          </div>
        </div>
      )}
    </div>
  );
}
