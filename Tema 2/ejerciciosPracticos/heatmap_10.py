import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# CARGA Y PREPARACIÓN DEL DATASET CLÍNICO
# Cargamos heart.csv:
# - 'age': Edad del paciente en años
# - 'trestbps': Presión arterial sistólica en reposo (mm Hg)
# - 'chol': Colesterol sérico en suero (mg/dl)
# - 'thalach': Frecuencia cardíaca máxima alcanzada (ppm)
# - 'oldpeak': Depresión del segmento ST inducida por el ejercicio

df = pd.read_csv('heart.csv')


# SELECCIÓN DE VARIABLES CONTINUAS Y CÁLCULO DE PEARSON
# Filtramos exclusivamente las variables continuas cuantitativas
# (evitando mezclar variables categóricas o binarias donde Pearson no es adecuado)
cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
corr_matrix = df[cols].corr(method='pearson')
# method='pearson', 'kendall' o 'spearman' 

# INSTANCIACIÓN DEL LIENZO
# Dimensiones casi cuadradas (7x6) para alojar una matriz de 5x5 más la barra de color
fig, ax = plt.subplots(figsize=(7.5, 6.5), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# RENDERIZADO DEL HEATMAP CON SEABORN
# - annot=True: Escribe el valor numérico exacto dentro de cada celda.
# - fmt='.2f': Formatea los valores a exactamente 2 decimales.
# - cmap='coolwarm': Paleta divergente canónica (azul = negativo, rojo = positivo).
# - vmin=-1, vmax=1: Fija los límites teóricos absolutos de la correlación de Pearson.
# - center=0: Garantiza que el color neutro (blanco/gris claro) corresponda al 0.00.
# - square=True: Fuerza celdas estrictamente cuadradas (evita rectángulos deformados).
# - linewidths=0.5: Añade una rejilla blanca milimétrica para separar las celdas.
# - cbar_kws={'shrink': 0.86}: Escala la barra de color para que encaje con la altura de la matriz.
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1.0,
    vmax=1.0,
    center=0.0,
    square=True,
    linewidths=0.5,
    linecolor='white',
    cbar_kws={'shrink': 0.86}, # El label se ha retirado de aquí para gestionarlo de forma independiente
    annot_kws={'size': 10, 'weight': 'bold', 'color': '#0F172A'},
    ax=ax
)

# SEPARACIÓN DEL LABEL EN LA BARRA DE COLOR
# Extraemos el objeto de la barra de color generada por Seaborn
cbar = ax.collections[0].colorbar
# Asignamos el texto y aplicamos labelpad para distanciarlo del eje numérico
cbar.set_label('Coeficiente de Pearson (r)', labelpad=14)


# AJUSTES TIPOGRÁFICOS Y DE ETIQUETAS
# Etiquetas limpias en español para sustituir los nombres técnicos de base de datos
etiquetas_legibles = ['Edad', 'Presión Reposo', 'Colesterol', 'Frec. Cardíaca', 'Depresión ST']
ax.set_xticklabels(etiquetas_legibles, rotation=30, ha='right', fontsize=9.5, color='#1E293B')
ax.set_yticklabels(etiquetas_legibles, rotation=0, va='center', fontsize=9.5, color='#1E293B')

# Título orientado a la acción (Storytelling): comunica el propósito analítico
ax.set_title(
    'Matriz de Correlación Bivariada en Variables de Salud Cardíaca',
    x=-0.10,        # Desplaza el título hacia la izquierda (valores negativos salen de la caja)
    ha='left',      # Fuerza la alineación del texto a la izquierda desde la nueva coordenada X
    fontsize=12,
    fontweight='bold',
    pad=18,
    color='#0F172A'
)

# RENDERIZADO Y VISUALIZACIÓN
plt.tight_layout()
plt.show()