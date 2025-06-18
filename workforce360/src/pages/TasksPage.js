import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../App";

const API_URL = window.location.origin.replace(":3000", ":8000") + "/tasks";

export default function TasksPage() {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem("token");
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [add, setAdd] = useState(false);
  const [form, setForm] = useState({ title: "", description: "" });
  const [error, setError] = useState(null);

  // Fetch tasks
  useEffect(() => {
    setLoading(true);
    fetch(API_URL + "/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => {
        setTasks(data || []);
      })
      .catch(() => setError("Failed to load tasks"))
      .finally(() => setLoading(false));
  }, [add, token]);

  function handleInput(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  function handleAddTask(e) {
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
        if (!r.ok) throw new Error("Could not create task");
        return r.json();
      })
      .then(() => {
        setForm({ title: "", description: "" });
        setAdd((a) => !a); // reload list
      })
      .catch(() => setError("Failed to create task"));
  }

  return (
    <section>
      <h2>Tasks</h2>
      <form onSubmit={handleAddTask} style={{ marginBottom: 18, background: "#f1f3f6", borderRadius: 6, padding: 14, maxWidth: 450 }}>
        <strong>Add Task</strong>
        <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
          <input name="title" value={form.title} required placeholder="Title" onChange={handleInput} style={{ flex: 1 }} />
          <input name="description" value={form.description} placeholder="Description" onChange={handleInput} style={{ flex: 1 }} />
          <button type="submit" style={{ background: "#007bff", color: "#fff", border: 0, padding: "0 18px", borderRadius: 4 }}>Add</button>
        </div>
        {error && <div style={{ color: "red", marginTop: 6 }}>{error}</div>}
      </form>
      {loading ? (
        <div>Loading...</div>
      ) : tasks.length === 0 ? (
        <div>No tasks found.</div>
      ) : (
        <table className="wf360-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Status</th>
              <th>Assigned To</th>
              <th>Due</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((t) => (
              <tr key={t.id}>
                <td>{t.title}</td>
                <td>{t.description}</td>
                <td>
                  <StatusTag status={t.status} />
                </td>
                <td>{t.assigned_to_id || <span style={{ color: "#888" }}>Unassigned</span>}</td>
                <td>{t.due_date?.slice?.(0, 10)}</td>
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
  if (status === "open") color = "#007bff";
  if (status === "in_progress") color = "#17a2b8";
  if (status === "completed") color = "green";
  if (status === "archived") color = "#aaa";
  return (
    <span style={{ background: color, color: "#fff", borderRadius: 4, padding: "2px 8px", fontWeight: 500 }}>{status}</span>
  );
}
