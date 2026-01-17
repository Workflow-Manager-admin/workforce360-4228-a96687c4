import React, { useState, useEffect, createContext } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import TasksPage from "./pages/TasksPage";
import TimesheetPage from "./pages/TimesheetPage";
import LeavePage from "./pages/LeavePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { fetchMe } from "./api/auth";

// Color theme according to spec
const theme = {
  primary: "#007bff",
  secondary: "#6c757d",
  accent: "#17a2b8",
  lightBg: "#ffffff",
  navBg: "#f7fafc",
};

// Minimal global auth context for login/logout
export const AuthContext = createContext();

export default function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);

  // Check token on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setChecking(false);
      return;
    }
    fetchMe(token)
      .then(user => {
        setUser(user);
      })
      .finally(() => setChecking(false));
  }, []);

  // Logout handler
  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  if (checking) {
    return <div style={{ textAlign: "center", marginTop: 50 }}>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      <Router>
        <div className="wf360-root" style={{ background: theme.lightBg, minHeight: "100vh" }}>
          <NavBar user={user} onLogout={logout} theme={theme} />
          <main style={{ marginLeft: 220, padding: "2rem 2rem 0 2rem" }}>
            <Routes>
              <Route path="/login" element={user ? <Navigate to="/" /> : <LoginPage />} />
              <Route path="/register" element={user ? <Navigate to="/" /> : <RegisterPage />} />
              <Route path="/" element={user ? <DashboardPage /> : <Navigate to="/login" />} />
              <Route path="/tasks" element={user ? <TasksPage /> : <Navigate to="/login" />} />
              <Route path="/timesheets" element={user ? <TimesheetPage /> : <Navigate to="/login" />} />
              <Route path="/leaves" element={user ? <LeavePage /> : <Navigate to="/login" />} />
              <Route path="*" element={<div>Page not found</div>} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthContext.Provider>
  );
}

// Navigation bar/side panel with minimal styles for MVP
function NavBar({ user, onLogout, theme }) {
  return (
    <nav
      className="wf360-nav"
      style={{
        width: 200,
        position: "fixed",
        top: 0,
        left: 0,
        height: "100vh",
        background: theme.navBg,
        borderRight: `1px solid #e5e7eb`,
        paddingTop: "2rem",
        zIndex: 100,
      }}
    >
      <div style={{ marginBottom: "2rem", textAlign: "center", fontWeight: 700 }}>
        <span style={{ color: theme.primary, fontSize: 20 }}>WorkForce360</span>
      </div>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {user && (
          <>
            <li>
              <NavItem to="/" label="Dashboard" icon="🏠" theme={theme} />
            </li>
            <li>
              <NavItem to="/tasks" label="Tasks" icon="📝" theme={theme} />
            </li>
            <li>
              <NavItem to="/timesheets" label="Timesheets" icon="🕑" theme={theme} />
            </li>
            <li>
              <NavItem to="/leaves" label="Leave" icon="🌴" theme={theme} />
            </li>
          </>
        )}
      </ul>
      <div style={{ position: "absolute", bottom: 40, width: "100%", textAlign: "center" }}>
        {user ? (
          <div>
            <div
              style={{
                fontSize: "0.95em",
                marginBottom: 8,
                color: theme.secondary,
                wordBreak: "break-word",
              }}
            >
              {user.full_name || user.username}
            </div>
            <button
              style={{
                background: theme.secondary,
                color: "#fff",
                border: 0,
                borderRadius: 4,
                padding: "0.4em 1.2em",
                fontWeight: 500,
                cursor: "pointer",
              }}
              onClick={onLogout}
            >
              Logout
            </button>
          </div>
        ) : (
          <>
            <Link to="/login">
              <button
                style={{
                  background: theme.primary,
                  color: "#fff",
                  border: 0,
                  borderRadius: 4,
                  padding: "0.4em 1.2em",
                  marginRight: 8,
                  fontWeight: 500,
                }}
              >
                Login
              </button>
            </Link>
            <Link to="/register">
              <button
                style={{
                  background: theme.accent,
                  color: "#fff",
                  border: 0,
                  borderRadius: 4,
                  padding: "0.4em 1.2em",
                  fontWeight: 500,
                }}
              >
                Register
              </button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

function NavItem({ to, label, icon, theme }) {
  return (
    <Link
      to={to}
      style={{
        display: "flex",
        alignItems: "center",
        padding: "0.75em 1.5em",
        textDecoration: "none",
        color: theme.primary,
        marginBottom: 8,
        fontWeight: 500,
        borderRadius: 5,
        transition: "background 0.2s",
      }}
      activeclassname="active"
    >
      <span style={{ marginRight: 10 }}>{icon}</span>
      {label}
    </Link>
  );
}
