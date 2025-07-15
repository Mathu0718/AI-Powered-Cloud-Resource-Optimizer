import React, { useEffect, useState } from "react";
import {
  fetchReport,
  fetchStatus,
  triggerCleanup,
  fetchCSVandEmail,
} from "./api";

export default function Dashboard() {
  const [report, setReport] = useState([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [cleanupLoading, setCleanupLoading] = useState(false);
  const [csvLoading, setCSVLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [reportData, statusData] = await Promise.all([
        fetchReport(),
        fetchStatus(),
      ]);
      setReport(reportData);
      setStatus(statusData.status || statusData.message || "No status available");
    } catch (error) {
      console.error("Error loading data:", error);
      setStatus("❌ Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const handleCleanup = async () => {
    setCleanupLoading(true);
    setStatus("⚙️ Triggering cleanup...");
    try {
      const data = await triggerCleanup();
      alert(data.message || "Cleanup operation completed");
      setStatus(data.message || "Cleanup complete");
      await loadData();
    } catch (error) {
      console.error("Cleanup error:", error);
      alert("❌ Cleanup failed.");
      setStatus("❌ Cleanup failed.");
    } finally {
      setCleanupLoading(false);
    }
  };

  const handleGetCSV = async () => {
    setCSVLoading(true);
    try {
      const data = await fetchCSVandEmail();
      alert(data.message || "CSV sent to email");
      if (data.report) setReport(data.report);
    } catch (error) {
      console.error("CSV fetch/send error:", error);
      alert("❌ Failed to fetch/send CSV");
    } finally {
      setCSVLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">📊 Cloud Cleaner Dashboard</h1>

      <div className="flex items-center space-x-4 mb-4">
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          onClick={handleCleanup}
          disabled={cleanupLoading}
        >
          {cleanupLoading ? "🧹 Cleaning..." : "Trigger Cleanup"}
        </button>

        <button
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
          onClick={handleGetCSV}
          disabled={csvLoading}
        >
          {csvLoading ? "📤 Sending CSV..." : "Get Current Cost CSV"}
        </button>
      </div>

      <p className="mb-5 text-gray-700">Status: {status}</p>

      {loading ? (
        <p>Loading report...</p>
      ) : (
        <div className="overflow-x-auto border rounded">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-semibold">Service</th>
                <th className="px-4 py-2 text-left text-sm font-semibold">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {report.length === 0 ? (
                <tr>
                  <td colSpan="2" className="p-4 text-center text-gray-500">
                    No data available
                  </td>
                </tr>
              ) : (
                report.map((row, idx) => (
                  <tr key={idx}>
                    <td className="px-4 py-2 whitespace-nowrap">{row.service}</td>
                    <td className="px-4 py-2">{row.details}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
