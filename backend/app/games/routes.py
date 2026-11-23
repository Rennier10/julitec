"""API de videojuegos (protegida con JWT).
GET  /api/games?q=&category=&platform=   catálogo con búsqueda y filtros
GET  /api/games/top?platform=&limit=      más vendidos / top (por plataforma)
GET  /api/games/new                       últimos estrenos (GTA VI, FC 27...)
GET  /api/games/platforms                 plataformas disponibles
GET  /api/games/<id>                      detalle
POST /api/orders                          tramitar pedido (simulación)"""
import uuid, datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .data import GAMES, ALL

games_bp = Blueprint("games", __name__, url_prefix="/api/games")

def _filter(items, platform=None):
    return [g for g in items if not platform or platform in g["platforms"]]

@games_bp.get("")
@jwt_required()
def list_games():
    q = request.args.get("q", "").lower()
    cat = request.args.get("category")
    items = [g for g in _filter(GAMES, request.args.get("platform"))
             if q in g["title"].lower() and (not cat or g["category"] == cat)]
    return jsonify(count=len(items), games=items)

@games_bp.get("/top")
@jwt_required()
def top():
    limit = request.args.get("limit", 10, type=int)
    items = sorted(_filter(GAMES, request.args.get("platform")), key=lambda g: g["rank"])[:limit]
    return jsonify(count=len(items), games=items)

@games_bp.get("/new")
@jwt_required()
def new():
    return jsonify(games=sorted([g for g in GAMES if g["new"]], key=lambda g: g["release"], reverse=True))

@games_bp.get("/platforms")
@jwt_required()
def platforms():
    return jsonify(platforms=ALL)

@games_bp.get("/<int:gid>")
@jwt_required()
def detail(gid):
    g = next((g for g in GAMES if g["id"] == gid), None)
    return (jsonify(g), 200) if g else (jsonify(msg="Juego no encontrado"), 404)

# ── Pedidos ────────────────────────────────────────────────────────────────────
orders_bp = Blueprint("orders", __name__, url_prefix="/api")

@orders_bp.post("/orders")
@jwt_required()
def place_order():
    """Recibe la cesta y devuelve una confirmación simulada con número de pedido."""
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not items:
        return jsonify(msg="La cesta está vacía"), 400

    # Validar y recalcular totales en el servidor (no confiar en el cliente)
    line_items = []
    total = 0
    for item in items:
        gid = item.get("game_id")
        plat = item.get("platform")
        g = next((g for g in GAMES if g["id"] == gid), None)
        if not g or plat not in g["prices"]:
            return jsonify(msg=f"Juego o plataforma inválidos (id={gid}, plat={plat})"), 400
        price = g["prices"][plat]
        total += price
        line_items.append({"title": g["title"], "platform": plat, "price": price})

    order_id = f"JUL-{uuid.uuid4().hex[:8].upper()}"
    return jsonify(
        order_id=order_id,
        status="confirmed",
        items=line_items,
        total=total,
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        message="¡Pedido confirmado! Recibirás las claves de activación en tu correo.",
    ), 201
