# JULITEC · Entrega final · Ingeniería Web II
Tienda de videojuegos (estilo Loaded): **React + Vite** · **Flask + JWT** · **Docker/Compose** · **Kubernetes** · **GitHub Actions**.
Login demo: `admin@julitec.com` / `Admin123!` (cambiable con `DEMO_EMAIL`, `DEMO_PASSWORD`).

## Estructura
`backend/` API Flask (auth, games, tests) · `frontend/` React · `k8s/julitec.yaml` · `docker-compose.yml` · `.github/workflows/ci.yml`

## Ejecutar
- **Local:** `cd backend && pip install -r requirements.txt && python run.py` y `cd frontend && npm install && npm run dev` (http://localhost:5173)
- **Docker Compose:** `docker compose up --build` → http://localhost:8080
- **Kubernetes (minikube / Docker Desktop):** construir imágenes (o usar las de GHCR), editar `TU_USUARIO` en `k8s/julitec.yaml`, `kubectl apply -f k8s/julitec.yaml`, `kubectl get pods -n julitec` → http://localhost:30080 (`minikube service frontend -n julitec`)

## API (todas con `Authorization: Bearer <JWT>`)
`POST /api/auth/login` · `GET /api/auth/me` · `GET /api/games?q=&category=&platform=` · **`GET /api/games/top?platform=PS5&limit=10`** (más vendidos por plataforma) · `GET /api/games/new` (estrenos GTA VI y EA FC 27) · `GET /api/games/<id>` · `GET /api/health`
Plataformas: PC, PS5, PS4, XBOX, SWITCH. Portadas reales: guardar `frontend/public/covers/<id>.jpg` (GTA VI = 1, FC 27 = 2); si no existe se muestra la portada generada.

## Qué explicar por sesión
- **S9 Nube:** IaaS (AWS EC2, GCE, Azure VM: tú administras SO y runtime), PaaS (Elastic Beanstalk, App Engine, Azure App Service: subes código), SaaS (GitHub, Gmail: solo usas). Julitec en la nube: Kubernetes administrado (EKS/GKE/AKS) = IaaS+PaaS; GHCR = SaaS.
- **S10 Docker:** imagen = plantilla inmutable (`Dockerfile`), contenedor = instancia; volumen `julitec_logs` persiste logs; Compose levanta backend + frontend en una red con un solo comando; multi-stage reduce el tamaño del frontend.
- **S11 Kubernetes:** Pod = unidad mínima; Deployment = réplicas + rolling updates; Service = IP/DNS estable (`backend`) y balanceo; Secret = clave JWT; probes = autorecuperación; HPA = autoescalado.
- **S12 Git/GitFlow:** `main` (producción) · `develop` (integración) · `feature/*` · `release/*` · `hotfix/*`. Ej.: `git checkout -b feature/catalogo-top develop` → PR a `develop` → release → merge a `main` + tag `v1.0.0`.
- **S13 CI/CD:** cada push/PR corre pytest y build del frontend; en `main` construye y publica las imágenes en GHCR (CD); el despliegue final es `kubectl apply`/`rollout restart`.

## Seguridad / trabajo futuro
Cambiar `JWT_SECRET_KEY` en producción (Secret). Datos del catálogo y precios son demostrativos; pendiente: BD persistente, registro de usuarios, pagos reales.
