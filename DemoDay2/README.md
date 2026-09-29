# Observatorio de Cohesión y Convergencia Europea (2000–2024)
### Demo Day 2: El Salto al Desarrollo Interactivo (70% Evaluación)
**Asignatura:** Visualización y Análisis de Datos (VAD)  
**Institución:** Universidad Politécnica de Madrid (UPM)  
**Autor:** Javier  

---

## 🎯 Pregunta y Soporte a la Decisión
* **Pregunta Central:** ¿Se está cerrando la brecha territorial entre las macrorregiones europeas? ¿En qué palancas estratégicas debe priorizar la inversión un fondo de cohesión pública?
* **Público Objetivo:** Planificadores de políticas públicas, comisiones de cohesión de la UE y analistas socioeconómicos.
* **Decisión que Apoya:** Asignación focalizada de presupuestos hacia I+D tecnológica y refuerzo sociosanitario en regiones en transición.

---

## 🏗️ Arquitectura Técnica

* **Framework Web:** Plotly Dash nativo sobre servidor Flask / WSGI.
* **Servidor de Producción:** Gunicorn (2 workers, 2 threads).
* **Análisis Geoespacial:** Mapas interactivos en Folium encapsulados en iframe con popups HTML y coropletas continuas.
* **Inteligencia Empírica (ML):** Regresores Random Forest de Scikit-Learn ($R^2 = 0.937$) ejecutándose en segundo plano para simulaciones en tiempo real.
* **Contenerización:** Docker multi-plataforma listo para despliegue público (Render, Railway, Fly.io o VPS).

---

## 📁 Estructura del Directorio

```text
DemoDay2/
├── app.py                  # Servidor y aplicación web Dash completa
├── lab_sol.py              # Entrypoint alternativo de ejecución directa
├── model.py                # Entrenamiento y motor de inferencia ML (Random Forest)
├── descargar_datos.py      # Pipeline de ingesta y limpieza de datos (Banco Mundial)
├── requirements.txt        # Dependencias oficiales de producción (+ gunicorn)
├── Dockerfile              # Imagen Docker ligera lista para despliegue público
├── docker-compose.yml      # Configuración de arranque con Docker Compose
├── .dockerignore           # Exclusión de archivos innecesarios en la imagen
├── README.md               # Documentación del proyecto
└── data/
    ├── europe_macro_historical.csv  # 975 registros limpios (39 países × 25 años)
    ├── europe_geometries.geojson     # Polígonos geoespaciales sincronizados
    └── models_rf.joblib              # Modelos entrenados y métricas persistidas
```

---

## 🚀 Despliegue y Ejecución

### Opción A: Despliegue con Docker (Recomendado)
```bash
# Construir y levantar el contenedor
docker compose up --build

# O con Docker CLI directo:
docker build -t vad-demoday2 .
docker run -p 8050:8050 vad-demoday2
```
La aplicación quedará accesible en: `http://localhost:8050`

### Opción B: Despliegue en Plataformas Cloud Gratuitas / PaaS
El `Dockerfile` está preparado con detección dinámica de variable `$PORT`, lo que permite desplegar en 1 clic en:
* **Render:** Crear un *Web Service* conectando el repositorio GitHub, seleccionando entorno *Docker*.
* **Railway / Fly.io:** Detecta automáticamente el `Dockerfile` y expone el servicio con SSL gratuito.
* **Hugging Face Spaces:** Crear un Space tipo *Docker*, subir los archivos y queda público al instante.

### Opción C: Ejecución Local Directa
```bash
conda activate vad
python app.py
# o con Gunicorn en producción:
gunicorn --bind 0.0.0.0:8050 app:server
```
