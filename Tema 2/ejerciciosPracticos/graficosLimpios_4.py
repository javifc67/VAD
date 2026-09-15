# Configuración limpia de la rejilla y spines
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('usa-salary.csv')

top_10 = df.nlargest(10, 'salary')
fig, ax = plt.subplots(figsize=(8, 4.5))

# ACENTO DE COLOR ESTRATÉGICO
# Generamos la lista de colores iterando ÚNICAMENTE sobre el top_10.
# El estado líder (índice 0) va en rojo de alto contraste (#D92121),
# y el resto de la muestra va en un gris neutro desaturado (#94A3B8).
colores = ['#D92121' if x == top_10['state'].iloc[0] else '#94A3B8' for x in top_10['state']]
# ['#D92121', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8']

# ORIENTACIÓN HORIZONTAL LIMPIA
# Pasamos la lista 'colores' al parámetro 'palette'.
sns.barplot(data=top_10, x='salary', y='state', hue='state', palette=colores, legend=False, ax=ax)

ax.set_title('Top 10 Estados de EE.UU. por salario', loc='left', pad=15)
ax.set_xlabel('Salario medio anual ($k)')
ax.set_ylabel('')  # Limpiamos el texto redundante del eje Y

# ELIMINAR BORDES (SPINES)
# Eliminamos exclusivamente el superior y el derecho.
# Mantenemos el izquierdo (nombres) y el inferior (eje base numérico).
sns.despine(ax=ax, top=True, right=True, left=False, bottom=False)

# OPTIMIZAR REJILLAS DE FONDO
ax.set_axisbelow(True)  # Asegura que la rejilla quede siempre por detrás

# Como las barras son horizontales, el ojo necesita ayuda para bajar 
# desde la punta de la barra hasta el eje X (abajo) para leer la magnitud.
# Por lo tanto, activamos la cuadrícula en el eje X y apagamos la del Y.
ax.xaxis.grid(True, color='#CBD5E1', linestyle='-', linewidth=0.8)
ax.yaxis.grid(False)    

plt.tight_layout()
plt.show()