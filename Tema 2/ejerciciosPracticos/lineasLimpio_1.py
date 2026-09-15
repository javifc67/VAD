# Trazado de líneas limpio en Python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm  # Librería necesaria para cálculos estadísticos avanzados

df = pd.read_csv('temperature-variation.csv')

fig, ax = plt.subplots(figsize=(8, 4.5))
# Dibujar variación y tendencia suavizada
ax.plot(df['Year'], df['Change'], color='#64748B', alpha=0.5, label='Variación anual')
# alpha=0.5 hace que la línea sea un 50% transparente (0 es invisible, 1 es sólido).
# La línea gris representa los datos crudos anuales (muy ruidosos). 
# Al hacerla semitransparente, la enviamos al "fondo" del lienzo visual. Sigue aportando 
# contexto, pero no ensucia el gráfico ni distrae. Así logramos que la línea roja (el suavizado), 
# que es totalmente opaca y más gruesa, salte a la vista inmediatamente como el mensaje principal.


# ax.plot(df['Year'], df['Lowess(5)'], color='#D92121', linewidth=2, label='Suavizado Lowess')

# CÁLCULO DEL SUAVIZADO LOWESS directamente desde los datos, sin usar la columna 'Lowess(5)' del CSV
# Usamos sm.nonparametric.lowess(endog, exog, frac)
#   - endog: Variable Y (Change)
#   - exog: Variable X (Year)
#   - frac: Es la "ventana" de datos que analiza cada vez. 
#           0.1 significa que usa el 10% de los puntos vecinos para calcular 
#           la línea en cada tramo. Si subes este número a 0.3, la línea 
#           será mucho más plana y rígida. Si lo bajas a 0.05, será muy nerviosa.
lowess_calculado = sm.nonparametric.lowess(df['Change'], df['Year'], frac=0.1)
# lowess_calculado nos devuelve una matriz (array 2D) con dos columnas:
#   - lowess_calculado[:, 0] son las coordenadas X
#   - lowess_calculado[:, 1] son las coordenadas Y suavizadas
ax.plot(lowess_calculado[:, 0], lowess_calculado[:, 1], color='#D92121',  linewidth=2.5, label='Suavizado Lowess (frac=0.1)')


# =====================================================================
# HITO CLAVE: MARCADORES EN MÁXIMO Y MÍNIMO (STORYTELLING)
# =====================================================================
# En visualización, el ojo busca instintivamente los valores extremos.
# En lugar de dejar que el alumno lo busque a ojo, lo calculamos y lo marcamos.

# Encontramos los índices (las filas) de los valores extremos
indice_max = df['Change'].idxmax()
indice_min = df['Change'].idxmin()

# Extraemos el Año (X) y la Temperatura (Y) exactos para ambos
año_maximo = df.loc[indice_max, 'Year']
temp_maxima = df.loc[indice_max, 'Change']

año_minimo = df.loc[indice_min, 'Year']
temp_minima = df.loc[indice_min, 'Change']

# Dibujamos puntos sutiles (marker='o') en esas coordenadas.
ax.plot(año_maximo, temp_maxima, marker='o', markersize=6, color='#1E293B')
ax.plot(año_minimo, temp_minima, marker='o', markersize=6, color='#1E293B')

# Añadimos anotaciones elegantes para explicar qué es cada punto.
# Anotación del Máximo
ax.annotate(
    f'Pico histórico ({año_maximo})', 
    xy=(año_maximo, temp_maxima), 
    xytext=(año_maximo - 20, temp_maxima + 0.15), # Desplazado arriba a la izquierda
    arrowprops=dict(
        arrowstyle="->", 
        color='#64748B', 
        connectionstyle="arc3,rad=-0.2"
    ),
    fontsize=9, 
    color='#334155', 
    fontweight='bold'
)

# Anotación del Mínimo
ax.annotate(
    f'Mínimo histórico ({año_minimo})', 
    xy=(año_minimo, temp_minima), 
    xytext=(año_minimo + 15, temp_minima), 
    va='center', 
    ha='left', # Hace que la caja de texto empiece a escribirse hacia la derecha
    arrowprops=dict(
        arrowstyle="->", 
        color='#64748B', 
        connectionstyle="arc3,rad=-0.2",
        # RELPOS (Relative Position): Es una tupla (X, Y) de 0.0 a 1.0
        # (0, 0.5) significa: ancla la flecha en el 0% del ancho (borde izquierdo)
        # y en el 50% de la altura (centro vertical) de la caja de texto.
        relpos=(0, 0.5) 
    ),
    fontsize=9, 
    color='#334155', 
    fontweight='bold'
)


# Limpieza y eliminación de spines (marcos)
sns.despine(ax=ax)
ax.legend(frameon=False)
plt.savefig('temperatura.png', dpi=300)
# DPI significa "Dots Per Inch" (Puntos Por Pulgada). Es el parámetro que 
# define la densidad de píxeles, es decir, la resolución de tu imagen final.
# - Sin parámetro (Matplotlib usa ~100 por defecto): 
#   Genera una imagen de baja resolución, muy "ligera" en megas. Está bien 
#   para salir del paso en la pantalla del portátil, pero si copias esa 
#   imagen en tu PowerPoint y la estiras, los textos y la curva roja se 
#   verán borrosos (pixelados).
# - dpi=300 (El estándar profesional): 
#   Inyecta el triple de densidad de píxeles. 300 DPI es el estándar de oro 
#   y el requisito mínimo absoluto para imprenta, revistas científicas o 
#   presentaciones de alto nivel. Garantiza que las líneas finas y los 
#   números de los ejes se vean nítidos y como cuchillos, incluso si el 
#   gráfico se proyecta en una pantalla de auditorio gigante.

plt.show()

