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

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY DemoDay2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y datasets desde DemoDay2
COPY DemoDay2/app.py DemoDay2/model.py DemoDay2/lab_sol.py ./
COPY DemoDay2/data/ ./data/

# Exponer el puerto
EXPOSE 8050

# Comprobación de salud para plataformas cloud
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT}/ || exit 1

# Comando de inicio con Gunicorn WSGI adaptado al puerto del entorno
CMD ["sh", "-c", "gunicorn --workers=2 --threads=2 --bind 0.0.0.0:${PORT} --timeout 120 app:server"]
