import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../App";

const API_URL = window.location.origin.replace(":3000", ":8000") + "/timesheets";

export default function TimesheetPage() {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [add, setAdd] = useState(false);
  const [form, setForm] = useState({ date: "", hours: 0, description: "" });
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(API_URL + "/", { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then((data) => setEntries(data || []))
      .catch(() => setError("Failed to load timesheets"))
      .finally(() => setLoading(false));
  }, [add, token]);

  function handleInput(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  function handleAddEntry(e) {
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
        setForm({ date: "", hours: 0, description: "" });
        setAdd((a) => !a);
      })
      .catch(() => setError("Failed to add entry"));
  }

  return (
    <section>
      <h2>Timesheets</h2>
      <form onSubmit={handleAddEntry} style={{ marginBottom: 18, background: "#f1f3f6", borderRadius: 6, padding: 14, maxWidth: 450 }}>
        <strong>Add Entry</strong>
        <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
          <input type="date" name="date" value={form.date} required onChange={handleInput} />
          <input type="number" min="0" name="hours" value={form.hours} required onChange={handleInput} placeholder="Hours" style={{ width: 75 }} />
          <input name="description" value={form.description} placeholder="Description" onChange={handleInput} style={{ flex: 1 }} />
          <button type="submit" style={{ background: "#17a2b8", color: "#fff", border: 0, padding: "0 18px", borderRadius: 4 }}>Add</button>
        </div>
        {error && <div style={{ color: "red", marginTop: 6 }}>{error}</div>}
      </form>
      {loading ? (
        <div>Loading...</div>
      ) : entries.length === 0 ? (
        <div>No entries found.</div>
      ) : (
        <table className="wf360-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Hours</th>
              <th>Description</th>
              <th>Task</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((e) => (
              <tr key={e.id}>
                <td>{e.date?.slice?.(0, 10)}</td>
                <td>{e.hours}</td>
                <td>{e.description}</td>
                <td>{e.task_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
