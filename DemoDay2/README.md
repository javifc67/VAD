# Observatorio de Cohesión y Convergencia Europea (2000–2024)
### Demo Day 2: El Salto al Desarrollo Interactivo
**Asignatura:** Visualización y Análisis de Datos (VAD) · Universidad Politécnica de Madrid (UPM)  
**Autor:** Javier  

🌐 **Despliegue Público en la Nube:** [https://vad-u2iv.onrender.com/](https://vad-u2iv.onrender.com/)

---

## 🎯 Pregunta y Soporte a la Decisión
* **Pregunta Central:** ¿Se está cerrando la brecha territorial entre las macrorregiones europeas? ¿En qué palancas estratégicas debe priorizar la inversión un fondo de cohesión pública?
* **Público Objetivo:** Planificadores de políticas públicas, comisiones de cohesión de la UE y analistas socioeconómicos.
* **Decisión que Apoya:** Asignación focalizada de presupuestos hacia I+D tecnológica y refuerzo sociosanitario en regiones en transición.

---

## 🏗️ Características del Cuadro de Mando
* **Arquitectura:** Aplicación interactiva nativa en Plotly Dash (servidor Flask).
* **Diagnóstico Espacial (Folium):** Mapa coroplético interactivo continuo con popups detallados por país y ranking territorial.
* **Línea Temporal con Reproductor Automático:** Avance interactivo con botones Play / Pausa para observar la evolución temporal 2000–2024 en tiempo real.
* **Dinámica Temporal (Plotly):** Dispersión multidimensional tipo Gapminder y comparativa de series históricas respecto a la media de la UE.

---

## 📁 Estructura del Proyecto
```text
├── lab_sol.py                          # Script principal de ejecución (entrypoint oficial)
├── app.py                              # Servidor y componentes de la aplicación Dash
├── requirements.txt                    # Dependencias y librerías de Python
├── README.md                           # Instrucciones de ejecución
└── data/
    ├── europe_macro_historical.csv     # Dataset histórico del Banco Mundial (2000–2024)
    └── europe_geometries.geojson       # Polígonos geoespaciales sincronizados
```

---

## 🚀 Instrucciones de Ejecución en Local

Para ejecutar la aplicación en local, abrir una terminal en el directorio del proyecto y seguir estos pasos:

### 1. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python lab_sol.py
```
*(Alternativamente, también puede iniciarse con `python app.py`)*

### 3. Abrir en el navegador
Una vez iniciado el servidor, acceder a la aplicación desde cualquier navegador en:  
👉 **http://localhost:8050** (o `http://127.0.0.1:8050`)
