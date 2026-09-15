import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu

# CARGA Y PREPARACIÓN DEL DATASET CLÍNICO
# Cargamos heart.csv:
# - 'condition': 0 = Sano / Sin enfermedad, 1 = Cardiopatía diagnosticada
# - 'thalach': Frecuencia cardíaca máxima alcanzada durante la prueba de esfuerzo
df = pd.read_csv('heart.csv')

# CÁLCULO INFERENCIAL: CONTRASTE DE HIPÓTESIS (MANN-WHITNEY U)
# Separamos los datos y calculamos si la diferencia es estadísticamente significativa
sanos = df[df['condition'] == 0]['thalach'].dropna()
enfermos = df[df['condition'] == 1]['thalach'].dropna()
stat, p_val = mannwhitneyu(sanos, enfermos, alternative='two-sided')

# Traducción del p-valor a notación convencional de asteriscos científicos
if p_val < 0.001:
    sig_text = '*** (p < 0.001)'
elif p_val < 0.01:
    sig_text = '** (p < 0.01)'
elif p_val < 0.05:
    sig_text = '* (p < 0.05)'
else:
    sig_text = 'ns (No significativo)'


# INSTANCIACIÓN DE SUBPLOTS COORDINADOS CON EJE Y COMPARTIDO
# - 1 fila, 2 columnas con sharey=True para fijar automáticamente la misma escala
#   vertical en ambos gráficos y permitir una comparación directa y rigurosa.
# - facecolor='#FAFAFA': Fondo neutro suave para descansar la vista.
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True, facecolor='#FAFAFA')

# Paleta preatencional:
# - '#94A3B8' (Gris Slate): Grupo control / Sano (línea base neutra).
# - '#D92121' (Rojo Crimson de alerta): Grupo patológico / Enfermo (foco de riesgo).
paleta_clinica = ['#94A3B8', '#D92121']

# SUBPLOT IZQUIERDO (axes[0]): DIAGRAMA DE CAJA (RESUMEN ESTADÍSTICO DE 5 NÚMEROS)
# Muestra mediana (línea central Q2), IQR (caja Q1-Q3), bigotes (1.5*IQR) y valores atípicos.
sns.boxplot(
    data=df,
    x='condition',
    y='thalach',
    palette=paleta_clinica,
    width=0.45,            # Anchura contenida para no saturar el espacio
    fliersize=4,           # Tamaño visible pero discreto para los outliers
    linewidth=1.2,
    ax=axes[0]
)

# Configuración y formateo del subplot de caja
axes[0].set_facecolor('#FAFAFA')
axes[0].set_title('Resumen Estadístico: Frecuencia Cardíaca (Caja)', loc='left', fontsize=11.5, weight='bold', pad=12)
axes[0].set_xlabel('Diagnóstico Clínico', fontsize=10, color='#1E293B', labelpad=8)
axes[0].set_ylabel('Frecuencia Cardíaca Máx. (ppm)', fontsize=10, color='#1E293B', labelpad=8)

# Etiquetas de categorías explícitas (en lugar de números crudos 0 y 1)
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(['Sano (0)', 'Enfermo (1)'], fontsize=10, weight='bold')

# Rejilla tenue horizontal para facilitar la lectura de la mediana y cuartiles
axes[0].grid(True, axis='y', linestyle=':', alpha=0.35, color='#94A3B8')

# SUBPLOT DERECHO (axes[1]): DIAGRAMA DE VIOLÍN (DENSIDAD CONTINUA KDE)
# Añade a la caja la estimación de densidad de kernel a ambos lados del eje central.
sns.violinplot(
    data=df,
    x='condition',
    y='thalach',
    palette=paleta_clinica,
    inner='quartile',       # Dibuja líneas discontinuas en la mediana y cuartiles dentro del violín
    cut=0,                  # Limita el violín al rango de datos observados (no extrapola fuera de límites)
    linewidth=1.2,
    ax=axes[1]
)

# Configuración y formateo del subplot de violín
axes[1].set_facecolor('#FAFAFA')
axes[1].set_title('Perfil de Densidad y Dispersión (Violín)', loc='left', fontsize=11.5, weight='bold', pad=12)
axes[1].set_xlabel('Diagnóstico Clínico', fontsize=10, color='#1E293B', labelpad=8)
axes[1].set_ylabel('')  # Vacío para evitar redundancia gráfica (comparten el eje Y con axes[0])

# Etiquetas de categorías sincronizadas
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(['Sano (0)', 'Enfermo (1)'], fontsize=10, weight='bold')

# Rejilla tenue horizontal alineada
axes[1].grid(True, axis='y', linestyle=':', alpha=0.35, color='#94A3B8')

# ANOTACIÓN AUTOMATIZADA DEL P-VALOR Y CORCHETE DE SIGNIFICANCIA EN AMBOS SUBPLOTS
y_max = df['thalach'].max()
y_bracket = y_max + 6
y_text = y_bracket + 3

for ax in axes:
    # Dibuja el corchete estadístico conectando x=0 y x=1
    ax.plot([0, 0, 1, 1], [y_bracket - 3, y_bracket, y_bracket, y_bracket - 3], lw=1.2, color='#0F172A')
    # Inserta el texto con la etiqueta de significancia
    ax.text(0.5, y_text, sig_text, ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#C51130' if p_val < 0.05 else '#475569')
    # Expande ligeramente el límite superior del eje Y para alojar la anotación sin cortes
    ax.set_ylim(top=y_text + 12)

# HIGIENE GRÁFICA Y REDUCCIÓN RADICAL DE TINTA (DATA-INK RATIO)
# Limpieza simultánea de marcos superior y derecho en ambos subplots a nivel de figura
sns.despine(fig=fig)

# Atenuación de ticks numéricos
for ax in axes:
    ax.tick_params(colors='#475569', labelsize=9.5)

# Título global orientado a la conclusión clínica (Storytelling)
fig.suptitle(
    'Impacto Cardíaco: Los pacientes con cardiopatía alcanzan frecuencias máximas sensiblemente inferiores',
    fontsize=13,
    weight='bold',
    color='#0F172A',
    y=0.98
)

# Ajuste automático de márgenes para evitar solapamientos
plt.tight_layout()
plt.show()