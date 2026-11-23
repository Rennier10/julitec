import { useState } from "react";
import { login } from "../services/api.js";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("admin@julitec.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const submit = async (e) => {
    e.preventDefault();
    try { onLogin((await login(email, password)).access_token); }
    catch { setError("Credenciales inválidas"); }
  };
  return (
    <div className="login">
      <form className="login-box" onSubmit={submit}>
        <h1 className="logo">JULITEC<span>.</span></h1>
        <p>PAY LESS. GAME MORE.</p>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Correo" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Contraseña" />
        {error && <small className="err">{error}</small>}
        <button className="buy">Iniciar sesión</button>
        <small>🔒 Autenticación protegida mediante JWT</small>
      </form>
    </div>
  );
}
