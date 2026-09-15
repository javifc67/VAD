# Gráfico de barras horizontales limpio
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('usa-salary.csv')

top_10 = df.nlargest(10, 'salary')
print(top_10)
fig, ax = plt.subplots(figsize=(8, 4.5))

# Barras horizontales para nombres de estados
sns.barplot(data=top_10, x='salary', y='state', color='#00629B', ax=ax)

sns.despine(ax=ax)
ax.set_title('Top 10 Estados de EE.UU. por salario', loc='left', pad=15)
ax.set_xlabel('Salario medio anual ($k)')
# ax.set_ylabel('Estado')
# tight_layout() fuerza a Matplotlib a expandir 
# los márgenes de la figura para que todos los nombres (tick labels) 
# quepan perfectamente dentro del cuadro visible.
plt.tight_layout()
plt.show()
