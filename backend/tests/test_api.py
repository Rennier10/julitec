"""Pruebas automáticas (se ejecutan en GitHub Actions): pytest"""
import pytest
from app import create_app

@pytest.fixture
def client():
    return create_app().test_client()

def _token(c):
    return c.post("/api/auth/login", json={"email": "admin@julitec.com", "password": "Admin123!"}).json["access_token"]

def test_sin_token_401(client):
    assert client.get("/api/games").status_code == 401

def test_login_malo(client):
    assert client.post("/api/auth/login", json={"email": "x", "password": "y"}).status_code == 401

def test_top_ps5(client):
    r = client.get("/api/games/top?platform=PS5", headers={"Authorization": f"Bearer {_token(client)}"})
    assert r.status_code == 200 and r.json["games"][0]["title"] == "Grand Theft Auto VI"

def test_estrenos(client):
    r = client.get("/api/games/new", headers={"Authorization": f"Bearer {_token(client)}"})
    assert {"Grand Theft Auto VI", "EA SPORTS FC 27"} <= {g["title"] for g in r.json["games"]}
