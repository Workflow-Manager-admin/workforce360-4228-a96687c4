const API_BASE =
  typeof window !== "undefined"
    ? window.location.origin.replace(":3000", ":8000") + "/auth"
    : "/auth";

// PUBLIC_INTERFACE
export async function login(email, password) {
  // The FastAPI backend expects form data (not JSON) with username and password keys
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const resp = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  if (!resp.ok) {
    throw new Error("Invalid credentials");
  }
  return resp.json(); // { access_token, token_type }
}

// PUBLIC_INTERFACE
export async function register(payload) {
  const resp = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!resp.ok) {
    const msg = await resp.text();
    throw new Error(msg || "Registration failed");
  }
  return resp.json();
}

// PUBLIC_INTERFACE
export async function fetchMe(token) {
  if (!token) return null;
  const resp = await fetch(`${API_BASE}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (resp.ok) return resp.json();
  return null;
}
