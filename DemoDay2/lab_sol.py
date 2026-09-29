"""
Demo Day 2: Observatorio de Cohesión y Convergencia Europea (2000-2024)
Punto de entrada alternativo compatible con la rúbrica oficial ('lab_sol.py').
Ejecuta el servidor web Plotly Dash con soporte de reactividad en tiempo real.
"""

from app import app, server

if __name__ == '__main__':
    print("Iniciando Observatorio de Cohesión Europea en http://127.0.0.1:8050 ...")
    app.run(debug=True, host='0.0.0.0', port=8050)
