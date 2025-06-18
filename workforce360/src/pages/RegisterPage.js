import React, { useState, useContext } from "react";
import { register, login, fetchMe } from "../api/auth";
import { AuthContext } from "../App";
import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const [form, setForm] = useState({ username: "", full_name: "", email: "", password: "" });
  const [err, setErr] = useState("");
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  function handleInput(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleRegister(e) {
    e.preventDefault();
    setErr("");
    try {
      await register(form);
      // After registration, auto-login
      const loginResp = await login(form.email, form.password);
      localStorage.setItem("token", loginResp.access_token);
      const user = await fetchMe(loginResp.access_token);
      setUser(user);
      navigate("/");
    } catch (e) {
      setErr("Registration failed: " + (e.message || ""));
    }
  }

  return (
    <section style={{ maxWidth: 440, margin: "40px auto" }}>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <label>
          Username<br />
          <input
            name="username"
            autoFocus
            value={form.username}
            onChange={handleInput}
            required
            style={{ width: "100%" }}
            placeholder="jdoe"
          />
        </label>
        <br />
        <label>
          Full Name<br />
          <input
            name="full_name"
            value={form.full_name}
            onChange={handleInput}
            required
            style={{ width: "100%" }}
            placeholder="John Doe"
          />
        </label>
        <br />
        <label>
          Email<br />
          <input
            name="email"
            value={form.email}
            type="email"
            onChange={handleInput}
            required
            style={{ width: "100%" }}
            placeholder="you@example.com"
          />
        </label>
        <br />
        <label>
          Password<br />
          <input
            name="password"
            value={form.password}
            type="password"
            onChange={handleInput}
            required
            style={{ width: "100%" }}
          />
        </label>
        <br />
        <button style={{ background: "#17a2b8", color: "#fff", border: 0, borderRadius: 4, padding: "0.5em 1.5em", fontWeight: 500, marginTop: 8 }} type="submit">
          Register
        </button>
        {err && <div style={{ marginTop: 8, color: "red" }}>{err}</div>}
      </form>
      <div style={{ marginTop: 16 }}>
        <span>Already have an account?</span> &nbsp;<a href="/login">Login</a>
      </div>
    </section>
  );
}
