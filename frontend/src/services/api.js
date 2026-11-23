// Cliente Axios: añade el JWT (Bearer) a cada petición y cierra sesión si el token expira (401).
import axios from "axios";
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "/api" });
api.interceptors.request.use((c) => {
  const t = localStorage.getItem("token");
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
api.interceptors.response.use((r) => r, (e) => {
  if (e.response?.status === 401 && localStorage.getItem("token")) { localStorage.removeItem("token"); location.reload(); }
  return Promise.reject(e);
});
export const login = (email, password) => api.post("/auth/login", { email, password }).then((r) => r.data);
export const getGames = (params) => api.get("/games", { params }).then((r) => r.data.games);
export const getTop = (platform) => api.get("/games/top", { params: { platform, limit: 10 } }).then((r) => r.data.games);
export const getNew = () => api.get("/games/new").then((r) => r.data.games);
export const placeOrder = (items) =>
  api.post("/orders", { items }).then((r) => r.data);
