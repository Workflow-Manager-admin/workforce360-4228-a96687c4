import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../App";

function useDashboardData(token) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    fetch(
      window.location.origin.replace(":3000", ":8000") + "/dashboard/summary",
      { headers: { Authorization: `Bearer ${token}` } }
    )
      .then((r) => r.json())
      .then(setSummary)
      .catch(setErr)
      .finally(() => setLoading(false));
  }, [token]);
  return { summary, loading, err };
}

export default function DashboardPage() {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const { summary, loading, err } = useDashboardData(token);

  return (
    <section>
      <h2>Dashboard Overview</h2>
      {loading && <p>Loading...</p>}
      {err && <p style={{ color: "red" }}>Failed to load summary</p>}
      {summary && (
        <div className="wf360-dashboard-grid">
          {Object.entries(summary).map(([k, v]) => (
            <div key={k} className="wf360-dashboard-card">
              <div className="wf360-dashboard-stat-val">{v}</div>
              <div className="wf360-dashboard-stat-label">{k.replace(/_/g, " ")}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
