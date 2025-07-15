const API_BASE = "http://127.0.0.1:5000"; // Flask backend URL

export async function fetchReport() {
  const res = await fetch(`${API_BASE}/report`);
  if (!res.ok) throw new Error("❌ Failed to fetch report");
  return res.json();
}

export async function fetchStatus() {
  const res = await fetch(`${API_BASE}/status`);
  if (!res.ok) throw new Error("❌ Failed to fetch status");
  return res.json();
}

export async function triggerCleanup() {
  const res = await fetch(`${API_BASE}/cleanup`, { method: "POST" });
  if (!res.ok) throw new Error("❌ Failed to trigger cleanup");
  return res.json();
}

// ✅ New function to fetch the current CSV and email it
export async function fetchCSVandEmail() {
  const res = await fetch(`${API_BASE}/get-csv`);
  if (!res.ok) throw new Error("❌ Failed to fetch/send CSV");
  return res.json();
}
