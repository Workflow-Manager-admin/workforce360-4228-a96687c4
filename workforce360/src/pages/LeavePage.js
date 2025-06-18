import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../App";

const API_URL = window.location.origin.replace(":3000", ":8000") + "/leaves";

export default function LeavePage() {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [add, setAdd] = useState(false);
  const [form, setForm] = useState({ start_date: "", end_date: "", reason: "" });
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(API_URL + "/", { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then((data) => setLeaves(data || []))
      .catch(() => setError("Failed to load leave requests"))
      .finally(() => setLoading(false));
  }, [add, token]);

  function handleInput(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  function handleAddLeave(e) {
    e.preventDefault();
    setError(null);
    fetch(API_URL + "/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    })
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then(() => {
        setForm({ start_date: "", end_date: "", reason: "" });
        setAdd((a) => !a);
      })
      .catch(() => setError("Failed to submit leave request"));
  }

  return (
    <section>
      <h2>Leave Requests</h2>
      <form onSubmit={handleAddLeave} style={{ marginBottom: 18, background: "#f1f3f6", borderRadius: 6, padding: 14, maxWidth: 450 }}>
        <strong>Request Leave</strong>
        <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
          <input type="date" name="start_date" value={form.start_date} required onChange={handleInput} />
          <input type="date" name="end_date" value={form.end_date} required onChange={handleInput} />
          <input name="reason" value={form.reason} placeholder="Reason" onChange={handleInput} style={{ flex: 1 }} />
          <button type="submit" style={{ background: "#6c757d", color: "#fff", border: 0, padding: "0 18px", borderRadius: 4 }}>Submit</button>
        </div>
        {error && <div style={{ color: "red", marginTop: 6 }}>{error}</div>}
      </form>
      {loading ? (
        <div>Loading...</div>
      ) : leaves.length === 0 ? (
        <div>No leave requests found.</div>
      ) : (
        <table className="wf360-table">
          <thead>
            <tr>
              <th>Start</th>
              <th>End</th>
              <th>Reason</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {leaves.map((l) => (
              <tr key={l.id}>
                <td>{l.start_date?.slice?.(0, 10)}</td>
                <td>{l.end_date?.slice?.(0, 10)}</td>
                <td>{l.reason}</td>
                <td>
                  <StatusTag status={l.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

function StatusTag({ status }) {
  let color = "#6c757d";
  if (status === "pending") color = "#007bff";
  if (status === "approved") color = "green";
  if (status === "rejected") color = "#dc3545";
  if (status === "cancelled") color = "#aaa";
  return (
    <span style={{ background: color, color: "#fff", borderRadius: 4, padding: "2px 8px", fontWeight: 500 }}>{status}</span>
  );
}
