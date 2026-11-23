// Tienda estilo Loaded: cabecera, plataformas, hero de estrenos, más vendidos, catálogo y cesta.
import { useEffect, useState } from "react";
import { getGames, getTop, getNew, placeOrder } from "../services/api.js";

const PLAT = { "": "Todas", PC: "PC", PS5: "PlayStation 5", PS4: "PlayStation 4", XBOX: "Xbox Series X|S", SWITCH: "Nintendo Switch" };
const cop = (n) => new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 }).format(n);

// Portada: intenta image_url (CDN) primero; si falla cae al gradiente con título.
function Cover({ g, plat }) {
  const [imgOk, setImgOk] = useState(true);
  const src = g.image_url || g.cover;
  return (
    <div className="cover" style={{ background: `linear-gradient(160deg, ${g.colors[0]}, ${g.colors[1]})` }}>
      {src && imgOk && (
        <img src={src} alt={g.title} onError={() => setImgOk(false)} />
      )}
      <b>{g.title}</b>
      {plat && <span className="tag">{PLAT[plat] || plat}</span>}
      {g.discount > 0 && <span className="off">{g.discount}% OFF</span>}
    </div>
  );
}

function Card({ g, filter, add }) {
  const [plat, setPlat] = useState(filter && g.platforms.includes(filter) ? filter : g.platforms[0]);
  useEffect(() => { if (filter && g.platforms.includes(filter)) setPlat(filter); }, [filter]);
  return (
    <div className="card">
      <Cover g={g} plat={plat} />
      <h3>{g.title}</h3>
      <select value={plat} onChange={(e) => setPlat(e.target.value)}>
        {g.platforms.map((p) => <option key={p} value={p}>{PLAT[p]}</option>)}
      </select>
      <div className="old">{cop(g.old_prices[plat])}</div>
      <div className="price">{cop(g.prices[plat])} {g.new && <em>NUEVO</em>}</div>
      <div className="row">
        <button onClick={() => add(g, plat)}>AÑADIR</button>
        <button className="buy" onClick={() => add(g, plat)}>COMPRAR</button>
      </div>
    </div>
  );
}

// Modal de confirmación de pedido exitoso
function OrderSuccess({ order, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="success-icon">✅</div>
        <h2>¡Pedido confirmado!</h2>
        <p className="order-id">N.° <strong>{order.order_id}</strong></p>
        <p className="order-msg">{order.message}</p>
        <div className="order-items">
          {order.items.map((it, k) => (
            <div key={k} className="order-line">
              <span>{it.title} <small>({it.platform})</small></span>
              <span>{cop(it.price)}</span>
            </div>
          ))}
        </div>
        <div className="order-total">Total pagado: <strong>{cop(order.total)}</strong></div>
        <button className="buy" style={{ width: "100%", marginTop: 18 }} onClick={onClose}>
          Seguir comprando
        </button>
      </div>
    </div>
  );
}

export default function Store({ onLogout }) {
  const [games, setGames] = useState([]);
  const [top, setTop] = useState([]);
  const [news, setNews] = useState([]);
  const [plat, setPlat] = useState("");
  const [q, setQ] = useState("");
  const [cart, setCart] = useState([]);
  const [open, setOpen] = useState(false);
  const [ordering, setOrdering] = useState(false);
  const [orderResult, setOrderResult] = useState(null);
  const [orderError, setOrderError] = useState("");

  useEffect(() => { getNew().then(setNews); }, []);
  useEffect(() => { getTop(plat || undefined).then(setTop); }, [plat]);
  useEffect(() => { getGames({ q, platform: plat || undefined }).then(setGames); }, [q, plat]);

  const add = (g, p) => { setCart((c) => [...c, { g, p }]); setOpen(true); };
  const total = cart.reduce((s, i) => s + i.g.prices[i.p], 0);
  const hero = news.find((n) => n.title.includes("Grand Theft")) || news[0];

  const handleCheckout = async () => {
    if (cart.length === 0) return;
    setOrdering(true);
    setOrderError("");
    try {
      const items = cart.map((i) => ({ game_id: i.g.id, platform: i.p }));
      const result = await placeOrder(items);
      setCart([]);
      setOpen(false);
      setOrderResult(result);
    } catch (err) {
      setOrderError(err.response?.data?.msg || "Error al procesar el pedido. Inténtalo de nuevo.");
    } finally {
      setOrdering(false);
    }
  };

  return (
    <>
      <header>
        <h1 className="logo">JULITEC<span>.</span></h1>
        <input className="search" placeholder="Buscar por título..." value={q} onChange={(e) => setQ(e.target.value)} />
        <span>COP</span>
        <button onClick={() => setOpen(true)}>🛒 {cart.length}</button>
        <button onClick={onLogout}>Salir</button>
      </header>
      <nav>
        {Object.entries(PLAT).map(([k, v]) => (
          <a key={k} className={plat === k ? "on" : ""} onClick={() => setPlat(k)}>{v}</a>
        ))}
      </nav>

      {hero && (
        <section className="hero" style={{ background: `linear-gradient(120deg, ${hero.colors[0]}, ${hero.colors[1]})` }}>
          <div>
            <small>ESTRENO · {hero.release}</small>
            <h2>{hero.title}</h2>
            <p>Disponible en {hero.platforms.map((p) => PLAT[p]).join(", ")}</p>
            <button className="buy" onClick={() => add(hero, plat && hero.platforms.includes(plat) ? plat : hero.platforms[0])}>
              COMPRAR AHORA
            </button>
          </div>
          <div className="mini">{news.map((n) => <Cover key={n.id} g={n} plat={n.platforms[0]} />)}</div>
        </section>
      )}

      <h2 className="sec">Los más vendidos {plat && `· ${PLAT[plat]}`}</h2>
      <div className="grid">{top.slice(0, 5).map((g) => <Card key={g.id} g={g} filter={plat} add={add} />)}</div>
      <h2 className="sec">Catálogo ({games.length})</h2>
      <div className="grid">{games.map((g) => <Card key={g.id} g={g} filter={plat} add={add} />)}</div>
      <footer>Julitec · Proyecto académico Ingeniería Web II · Universidad Manuela Beltrán</footer>

      {open && (
        <aside className="drawer">
          <button onClick={() => setOpen(false)}>✕</button>
          <h3>Mi cesta ({cart.length})</h3>
          {cart.length === 0 && <p style={{ opacity: 0.6 }}>La cesta está vacía.</p>}
          {cart.map((i, k) => (
            <p key={k}>
              {i.g.title} <small>{PLAT[i.p]}</small><br />
              {cop(i.g.prices[i.p])}{" "}
              <a onClick={() => setCart(cart.filter((_, x) => x !== k))}>🗑</a>
            </p>
          ))}
          {cart.length > 0 && <h3>SUBTOTAL {cop(total)}</h3>}
          {orderError && <p className="err">{orderError}</p>}
          <button
            className="buy"
            style={{ width: "100%", marginTop: 8, opacity: cart.length === 0 || ordering ? 0.5 : 1 }}
            disabled={cart.length === 0 || ordering}
            onClick={handleCheckout}
          >
            {ordering ? "Procesando…" : "TRAMITAR EL PEDIDO"}
          </button>
        </aside>
      )}

      {orderResult && (
        <OrderSuccess order={orderResult} onClose={() => setOrderResult(null)} />
      )}
    </>
  );
}
