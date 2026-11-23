# Imagen ligera de Python; capa de dependencias separada para aprovechar la caché de Docker
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser && mkdir -p /app/logs && chown -R appuser /app
USER appuser
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--access-logfile", "/app/logs/access.log", "run:app"]
