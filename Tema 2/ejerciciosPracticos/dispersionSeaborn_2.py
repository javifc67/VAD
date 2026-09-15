# Trazado de dispersión con Seaborn
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('world-happiness-report-2021.csv')

fig, ax = plt.subplots(figsize=(8, 4.5))

# Scatter plot bivariado
sns.scatterplot(data=df, x='Logged GDP per capita', y='Ladder score', hue='Regional indicator', 
                alpha=0.7, ax=ax)

# Correlación entre el dinero de un país y la felicidad de sus habitantes.
# EJE Y ('Ladder score'): 
# Es el índice oficial de Felicidad. Se mide usando la "Escala de Cantril" 
# (Cantril Ladder). Imagina una escalera del 0 al 10, donde 0 es la peor 
# vida posible y 10 es la mejor vida imaginable. Se le pregunta a los 
# ciudadanos en qué escalón sienten que están.
# EJE X ('Logged GDP per capita'):
# Es el Producto Interior Bruto (PIB) per cápita, pero transformado de 
# forma LOGARÍTMICA. 
# ¿Por qué logarítmico y no el dinero real? Porque la diferencia de riqueza 
# entre un país muy pobre y uno muy rico es tan gigantesca (exponencial) 
# que, si usáramos los dólares reales, los países pobres se aplastarían 
# todos a la izquierda del gráfico y los ricos se perderían por la derecha. 
# Al aplicar el logaritmo, "comprimimos" la escala del eje X para poder ver 
# una relación lineal mucho más clara en el gráfico.
# Scatter plot bivariado
# - hue: Colorea cada punto según su continente (Regional indicator),
#        lo que permite detectar clusters geográficos visualmente.

sns.despine(ax=ax)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 	frameon=False)

plt.tight_layout()
plt.show()