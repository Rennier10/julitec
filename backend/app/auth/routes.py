"""Autenticación JWT: /api/auth/login genera el token, /api/auth/me lo valida."""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
# Usuario de demostración (la BD real queda como trabajo futuro)
USER = {"id": 1, "email": os.getenv("DEMO_EMAIL", "admin@julitec.com"),
        "password": os.getenv("DEMO_PASSWORD", "Admin123!"), "name": "Administrador", "role": "admin"}

@auth_bp.post("/login")
def login():
    d = request.get_json(silent=True) or {}
    if d.get("email") != USER["email"] or d.get("password") != USER["password"]:
        return jsonify(msg="Credenciales inválidas"), 401
    token = create_access_token(identity=str(USER["id"]))
    return jsonify(access_token=token, user={k: USER[k] for k in ("id", "email", "name", "role")})

@auth_bp.get("/me")
@jwt_required()
def me():
    return jsonify(id=get_jwt_identity(), email=USER["email"], name=USER["name"], role=USER["role"])
