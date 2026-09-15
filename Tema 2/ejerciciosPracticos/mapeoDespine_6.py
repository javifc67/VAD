import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Carga del dataset real de la asignatura
df = pd.read_csv('world-happiness-report-2021.csv')

# Instanciación explícita del lienzo
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Mapeo semántico controlado con Seaborn
sns.scatterplot(
    data=df,
    x='Logged GDP per capita',
    y='Ladder score',
    hue='Regional indicator', # Primer nivel de agrupación: regiones
    size='Social support', # Segundo nivel de agrupación: apoyo social
    palette='Set2',
    sizes=(30, 250),
    alpha=0.85,
    ax=ax
)

# Línea de referencia y formato de ejes (reducción de carga cognitiva)
ax.axhline(y=6.0, color='#94A3B8', linestyle=':', alpha=0.8, linewidth=1.5)

# Texto desplazado a la izquierda
ax.text(6.5, 6.1, 'Felicidad alta (>= 6.0)', color='#64748B', fontsize=10, fontstyle='italic', ha='left')

# Título principal con estilo y alineación a la izquierda
ax.set_title('Relación Bivariada: Riqueza (PIB) frente a Felicidad Nacional', loc='left', fontsize=13, weight='bold', pad=15)

# Títulos de los ejes en negro puro para máxima legibilidad
ax.set_xlabel('PIB per cápita (escala logarítmica)', fontsize=10, color='black')
ax.set_ylabel('Índice de Felicidad (Ladder score)', fontsize=10, color='black')

# Eliminación de bordes e integración de rejilla sutil
sns.despine(ax=ax, top=True, right=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.3)

# Control avanzado de la leyenda
legend = ax.legend(
    # POSICIONAMIENTO EXTERNO (x, y)
    # Las coordenadas van de 0 a 1 respecto al tamaño de tu área de dibujo (ax).
    # - X = 1.03: Empuja la leyenda hacia la derecha, dejándola un 3% por fuera del borde del gráfico.
    # - Y = 1.00: La alinea verticalmente de forma exacta con el "techo" del gráfico.
    bbox_to_anchor=(1.03, 1),    
     # PUNTO DE ANCLAJE
    # Le indica a Matplotlib qué parte concreta de la caja de la leyenda 
    # debe clavar en la coordenada (1.03, 1) que hemos definido justo arriba.
    # Aquí le decimos: "Coge la esquina superior izquierda de la leyenda y ponla ahí".
    loc='upper left',
    # REDUCCIÓN DE RUIDO VISUAL
    # Elimina la línea o recuadro visible que suele rodear a las leyendas por defecto.
    frameon=False,
    # ORDEN TIPOGRÁFICO
    # Garantiza que todos los elementos de texto (títulos, nombres de países y números)
    # se alineen a la izquierda dentro de la leyenda.
    alignment='left'
)
        
       
# TRUCO DE DISEÑO AVANZADO
# Extraemos los marcadores visuales de la leyenda.
marcadores = getattr(legend, "legend_handles", getattr(legend, "legendHandles", []))
seccion_actual = None

# Emparejamos cada texto de la leyenda con su marcador visual
for texto, marcador in zip(legend.get_texts(), marcadores):
    etiqueta = texto.get_text()
    
    if etiqueta == 'Regional indicator':
        seccion_actual = 'region'
        texto.set_weight('bold')
        texto.set_size(11)
    elif etiqueta == 'Social support':
        seccion_actual = 'apoyo'
        # CORRECCIÓN: Inyectamos un salto de línea (\n) para generar espacio en blanco
        # antes del texto, separando visualmente ambos bloques de la leyenda.
        texto.set_text('\nSocial support')
        texto.set_weight('bold')
        texto.set_size(11)
    else:
        # Nombres de países o números
        texto.set_size(10)
        
        if seccion_actual == 'region':
            marcador.set_markersize(13) # Aumentamos el tamaño de los marcadores de región
         

plt.tight_layout()
plt.show()