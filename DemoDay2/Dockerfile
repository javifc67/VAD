# Imagen base oficial y ligera de Python
FROM python:3.11-slim

# Variables de entorno para optimizar Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8050

# Dependencias mínimas del sistema (curl para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y los datasets
COPY app.py model.py lab_sol.py ./
COPY data/ ./data/

# Exponer puerto por defecto
EXPOSE 8050

# Comprobación de salud para plataformas cloud (Render, Railway, Fly.io, etc.)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT}/ || exit 1

# Ejecución en producción con Gunicorn WSGI adaptado al puerto del entorno
CMD ["sh", "-c", "gunicorn --workers=2 --threads=2 --bind 0.0.0.0:${PORT} --timeout 120 app:server"]
