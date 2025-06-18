import React, { useState, useContext } from "react";
import { login, fetchMe } from "../api/auth";
import { AuthContext } from "../App";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  async function handleLogin(e) {
    e.preventDefault();
    setErr("");
    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      const user = await fetchMe(data.access_token);
      setUser(user);
      navigate("/");
    } catch (e) {
      setErr("Invalid email or password");
    }
  }

  return (
    <section style={{ maxWidth: 440, margin: "40px auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>
          Email<br />
          <input
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
            style={{ width: "100%" }}
            placeholder="you@example.com"
          />
        </label>
        <br />
        <label>
          Password<br />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            style={{ width: "100%" }}
          />
        </label>
        <br />
        <button style={{ background: "#007bff", color: "#fff", border: 0, borderRadius: 4, padding: "0.5em 1.5em", fontWeight: 500, marginTop: 8 }} type="submit">
          Login
        </button>
        {err && <div style={{ marginTop: 8, color: "red" }}>{err}</div>}
      </form>
      <div style={{ marginTop: 16 }}>
        <span>No account?</span> &nbsp;<a href="/register">Register</a>
      </div>
    </section>
  );
}
