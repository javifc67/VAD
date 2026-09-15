import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# CARGA Y PREPARACIÓN DE LOS DATOS REALES
# Cargamos el archivo usa-salary.csv (columnas: 'state' y 'salary')
df = pd.read_csv('usa-salary.csv')

# Filtramos los 6 estados con mayores ingresos y los ordenamos de mayor a menor
df_top = df.sort_values(by='salary', ascending=False).head(6)

# INSTANCIACIÓN DEL LIENZO Y GRÁFICO BASE CON SEABORN
fig, ax = plt.subplots(figsize=(9, 5), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Dibujamos las barras horizontales:
# Todas las barras nacen inicialmente en un gris neutro desaturado (#94A3B8)
# para no competir por la atención del espectador.
sns.barplot(
    data=df_top,
    x='salary',
    y='state',
    ax=ax,
    color='#94A3B8',
    edgecolor='none'
)

# APLICACIÓN DE FOCO PREATENCIONAL (COLOR DE ACENTO)
# ax.patches contiene la lista de rectángulos de las barras en orden de dibujado.
# La posición 0 es District of Columbia; la posición 1 es Washington (86.6k).
washington_bar = ax.patches[1]
washington_bar.set_facecolor('#C51130')


# ANOTACIONES NUMÉRICAS DIRECTAS AL FINAL DE LAS BARRAS
# Al rotular el dato exacto directamente sobre cada barra, eliminamos la necesidad
# de que el espectador tenga que bajar la vista al eje X para estimar el valor.
for bar in ax.patches:
    width = bar.get_width() # Ancho de la barra (valor del salario)
    ax.text(
        x=width + 1.2,                                # Desplazamiento sutil a la derecha de la barra
        y=bar.get_y() + bar.get_height() / 2,         # Centrado vertical dentro de la barra
        s=f'${width:.1f}k',                           # Formato numérico con prefijo de moneda y sufijo en miles
        va='center',
        ha='left',
        fontname='Arial',
        fontsize=10,
        fontweight='bold',
        color='#0F172A'
    )

# ANOTACIÓN SEMÁNTICA DIRECTA CON FLECHA INDICADORA
# Calculamos dinámicamente la esquina inferior derecha de la barra de Washington
x_arrow_target = washington_bar.get_width()
y_arrow_target = washington_bar.get_y() + washington_bar.get_height()


# Conectamos el insight explicativo directamente con el dato físico
ax.annotate(
    'Líder Costa Oeste\n(Hub tecnológico)',
    xy=(x_arrow_target, y_arrow_target),          # Apunta a la esquina inferior derecha
    xytext=(110, 1.6),                            # Donde se coloca el texto (coordenadas absolutas del lienzo)
    va='top',                                     # ALINEACIÓN VERTICAL CENTRADA
    ha='left',                                    # ALINEACIÓN HORIZONTAL (ancla la flecha a la izquierda del texto)    
    arrowprops=dict(
        facecolor='#C51130',
        edgecolor='#C51130',
        arrowstyle='->',
        lw=1.5,                                   # Grosor de la flecha
        connectionstyle='arc3,rad=-0.15'          # Curvatura sutil para no tapar texto
    ),
    fontsize=9.5,
    fontweight='bold',
    color='#C51130'
)

# LIMPIEZA RADICAL DE RUIDO VISUAL (DATA-INK RATIO)
# Ocultamos la escala numérica inferior del eje X ya que cada barra tiene su valor explícito
ax.xaxis.set_visible(False)

# Eliminamos todos los bordes exteriores (espinas) del gráfico
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(False)

# Ocultamos las marcas de ticks en el eje Y manteniendo legibles los nombres de los estados
ax.tick_params(axis='y', length=0, labelsize=10.5, labelcolor='#0F172A')

# Expandimos el límite horizontal en X para que el nuevo texto de la derecha tenga espacio de sobra
ax.set_xlim(0, 140)

# Eliminamos la etiqueta del eje Y por ser redundante y añadimos título orientado a la acción
ax.set_ylabel('')
ax.set_title(
    'Distribución Salarial en EE.UU.: Washington destaca tras la capital federal',
    loc='left',
    fontsize=12,
    fontweight='bold',
    pad=15,
    color='#0F172A'
)

plt.tight_layout()
plt.show()