import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./style.css";

// Attach the React app to the #app div
const container = document.getElementById("app");
const root = createRoot(container);
root.render(<App />);
