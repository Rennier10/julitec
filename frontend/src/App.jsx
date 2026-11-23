// Controla la sesión: sin token muestra Login, con token muestra la tienda.
import { useState } from "react";
import Login from "./pages/Login.jsx";
import Store from "./pages/Store.jsx";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const logout = () => { localStorage.removeItem("token"); setToken(null); };
  return token ? <Store onLogout={logout} /> :
    <Login onLogin={(t) => { localStorage.setItem("token", t); setToken(t); }} />;
}
