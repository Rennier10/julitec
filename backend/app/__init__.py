"""Application factory: crea y configura Flask, CORS, JWT y registra los módulos."""
import os, datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    # La clave sale de una variable de entorno (Secret en Kubernetes / .env en Compose)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-cambiar-en-produccion-0123456789")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)
    CORS(app)
    JWTManager(app)
    from .auth.routes import auth_bp
    from .games.routes import games_bp, orders_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(orders_bp)

    @app.get("/api/health")  # usado por los probes de Docker/Kubernetes
    def health():
        return jsonify(status="ok")
    return app
