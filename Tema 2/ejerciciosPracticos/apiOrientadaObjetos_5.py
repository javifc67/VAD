# Patrón de código estándar de la sesión 3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('japan-population.csv')


# En lugar de un solo gráfico, creamos una matriz (grid) visual.
# plt.subplots(1, 2) le dice a Matplotlib: "Dame 1 fila y 2 columnas".
# - 'fig' es el bastidor completo (la ventana de 13x5 pulgadas).
# - 'axes' es una lista con los 2 lienzos individuales (izquierdo y derecho).
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

año_minimo = df['year'].min()
año_maximo = df['year'].max()

# 2. SUBTRAMA 1 (axes[0]): EL CONTEXTO HISTÓRICO (MACRO)
# Usamos un gráfico de líneas porque estamos evaluando una tendencia a lo 
# largo de muchas décadas. La línea conecta los puntos y muestra la historia.
axes[0].plot(df['year'], df['pop_var'], color='#475569', linewidth=2)
axes[0].set_title('Evolución Histórica (1952-2020)', loc='left', fontsize=12, weight='bold')
axes[0].set_xlabel('Año')
axes[0].set_ylabel('Variación Neta de Población')

# Eje Y: Variación neta anual (personas ganadas/perdidas), no población total. >0 es crecimiento, <0 es declive.
# Misma escala Y en ambos paneles para permitir una comparación visual honesta y matemática del fenómeno.
# Variación = (Nacimientos + Inmigración) - (Muertes + Emigración)

# Bloqueamos el eje Y deliberadamente.
axes[0].set_ylim(-1000000, 1500000)

# ticks_auto_macro = axes[0].get_xticks()
# axes[0].set_xticks(list(ticks_auto_macro))

# Trazamos una línea base en el cero (origen). 
# Es crucial visualmente para que el ojo detecte al instante cuándo 
# Japón pasó de crecer (arriba) a perder población (abajo).
axes[0].axhline(0, color='#94A3B8', linestyle='--', linewidth=0.8)



# 3. SUBTRAMA 2 (axes[1]): EL ZOOM AL PROBLEMA (MICRO)
# Filtramos los datos para enfocarnos solo en el declive reciente.
df_recent = df[df['year'] >= 2000]

# Cambiamos a gráfico de barras. Al tener menos años, las barras separadas 
# enfatizan la magnitud física de la caída de población en cada periodo.
# Usamos color rojo (#C51130) por su semántica de "alerta" o "pérdida".
axes[1].bar(df_recent['year'], df_recent['pop_var'], color='#C51130', edgecolor='none')
axes[1].set_title('Declive Poblacional Reciente (>= 2000)', loc='left', fontsize=12, weight='bold')
axes[1].set_xlabel('Año')
# axes[1].set_ylabel('Variación Neta de Población')

# REGLA DE ORO DE LA VISUALIZACIÓN HONESTA:
# Sincronizamos exactamente el mismo límite del eje Y que en el gráfico 1.
# Si dejáramos que Matplotlib calculara la escala automáticamente aquí, 
# la caída parecería mucho más exagerada o minimizada. Al compartir escala, 
# la comparación visual entre ambos paneles es matemáticamente real.
axes[1].set_ylim(-1000000, 1500000) 

axes[1].axhline(0, color='#94A3B8', linestyle='--', linewidth=0.8)


# 4. LIMPIEZA DE RUIDO VISUAL (DATA-INK RATIO)
# Nota técnica: Al tener múltiples lienzos (subplots), le pasamos 'fig' 
# a despine para que elimine los bordes superior y derecho de TODOS los 
# gráficos a la vez, no solo del último que hayamos tocado.
sns.despine(fig=fig)

# Empuja los márgenes para que los textos no se monten unos sobre otros.
plt.tight_layout()

plt.show()