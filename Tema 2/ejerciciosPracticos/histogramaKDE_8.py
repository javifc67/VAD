import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Cierra cualquier bastidor o ventana gráfica previa que siga abierta en memoria
# plt.close('all')

# CARGA Y PREPARACIÓN DEL DATASET CLÍNICO
# Cargamos heart.csv (la columna 'chol' representa el colesterol sérico en mg/dl)
# El colesterol sérico es la cantidad de colesterol medida en la parte líquida de la sangre (el suero), en mg/dL.
# Incluye LDL y VLDL (“malos”), que pueden acumularse en las arterias, y HDL (“bueno”), que ayuda a retirarlo; los triglicéridos se miden por separado.
df = pd.read_csv('heart.csv')

# SIMULACIÓN DE UN SEGUNDO GRUPO PARA COMPARATIVA
# Restamos 40 mg/dl a toda la serie para simular un grupo de pacientes con niveles más bajos
df['chol_control'] = df['chol'] + 50


# INSTANCIACIÓN DEL LIENZO Y CONFIGURACIÓN BASE
fig, ax = plt.subplots(figsize=(8.5, 5), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# GENERACIÓN DEL HISTOGRAMA CON KDE SUPERPUESTO
# - bins=30: Granularidad óptima para capturar la distribución sin fragmentar en exceso.
# - kde=True: Traza la curva suave de densidad continua sobre las barras.
# - color='#00629B': Azul para una apariencia académica sobria.
# - alpha=0.45: Semitransparencia en las barras para que la línea continua destaque.
sns.histplot(
    data=df,
    x='chol',
    kde=True,
    # kde_kws={'bw_adjust': bw_factor}
    # bins=30,
    bins='auto',
    color='#00629B',
    alpha=0.45,
    edgecolor='white',
    linewidth=1.0,
    ax=ax
)
# Nota: bins puede ser:
# - Un entero (ej. bins=20):
#   Fuerza una cantidad fija y exacta de divisiones, ignorando la distribución
#   real de los datos.
# - Algoritmos estadísticos automáticos:
#   - 'auto': recomendado. Elige entre Sturges y Freedman-Diaconis según
#     el tamaño de la muestra.
#   - 'fd' (Freedman-Diaconis): usa el rango intercuartílico (IQR); robusto
#     ante valores atípicos extremos.
#   - 'sturges': método clásico; asume distribución aproximadamente normal.
#   - 'scott': se basa en la desviación estándar y el tamaño de muestra.
#   - 'rice': usa la raíz cúbica de 2*n; suele crear más barras.
#   - 'sqrt': usa la raíz cuadrada del número de observaciones.
# - Una lista de límites (ej. bins=[0, 2, 4, 6, 8, 10]):
#   Define manualmente el inicio y final de cada intervalo. Útil para
#   intervalos irregulares o rangos fijos, como notas.

# Nota: Cómo calcula KDE la curva (Estimación de Densidad por Kernel):
# Para cada punto del eje X, cada dato aporta un peso según su distancia.
# Usando una función de núcleo (kernel) gaussiano:
# peso = exp(-0.5 * ((x - dato) / ancho) ** 2)
# ¿QUÉ ES EL "ANCHO" (Ancho de banda o Bandwidth)?
# Es el parámetro crítico de suavizado que controla el radio de influencia de cada dato.
# - No se suele fijar un número a mano (como ancho=10), ya que depende de la escala de cada variable.
# - Se calcula de forma automática mediante algoritmos estadísticos (parámetro bw_method='scott' o 'silverman').
# - Un ancho demasiado pequeño genera una curva llena de picos falsos por el ruido.
# - Un ancho demasiado grande aplana la curva y borra los detalles reales de la distribución.
# Ejemplo: calcular la altura de la influencia en x=200, usando un ancho (bandwidth) de 10:
# dato=200  -> peso = 1.00  (está exactamente en 200)
# dato=202  -> peso = 0.98  (está muy cerca)
# dato=210  -> peso = 0.61  (está cerca)
# dato=220  -> peso = 0.14  (está más lejos)
# dato=240  -> peso = 0.00  (está demasiado lejos)
# La KDE suma los pesos normalizados de todos los datos de la muestra.
# Por eso la curva sube donde se concentran valores y baja en los vacíos.

# Ejemplo de cálculo del ancho de banda (bandwidth) aplicado por defecto en Seaborn:
from scipy.stats import gaussian_kde
# Aislamos los datos reales (eliminando nulos por seguridad matemática)
datos = df['chol'].dropna()
# Instanciamos el motor matemático exacto que usa Seaborn por defecto
estimador_kde = gaussian_kde(datos, bw_method='scott')
# El motor calcula un "factor" (un multiplicador basado en los datos).
# Para obtener el "ancho" absoluto en la misma escala que tu eje X (Felicidad), 
# lo multiplicamos por la desviación estándar de la muestra.
ancho_calculado = estimador_kde.factor * datos.std()
print(f"Regla automática utilizada: Scott")
print(f"Factor multiplicador: {estimador_kde.factor:.4f}")
print(f"ANCHO DE BANDA (Bandwidth) REAL APLICADO: {ancho_calculado:.4f}")


# GENERACIÓN DEL SEGUNDO HISTOGRAMA (GRUPO DE CONTROL - TIPO STEP)
# - element='step': Traza el contorno exterior como una escalera continua en lugar de barras individuales.
# - fill=False: Deja el interior transparente para evitar saturación visual y no tapar el grupo azul.
# - linestyle='--': Diferencia la línea para que destaque frente a la solidez del primer grupo.
# sns.histplot(
#     data=df,
#     x='chol_control',
#     kde=True,
#     bins='auto',
#     element='step',
#     fill=False,
#     color="#FF7300",  # Rojo teja para generar contraste
#     linewidth=1.5,
#     alpha=0.8,
#     label='Grupo Control (Simulado)',
#     ax=ax
# )
#for line in ax.lines:
#    line.set_linewidth(2.0)


# INCORPORACIÓN DE UMBRAL CLÍNICO DE REFERENCIA
# Umbral médico estándar: Colesterol deseable < 200 mg/dl (riesgo moderado/alto >= 200)
ax.axvline(x=200, color='#C51130', linestyle='--', linewidth=1.5, alpha=0.85)

# Anotación explicativa directa sobre la línea de corte
ax.text(
    x=195, # Posición horizontal; queda a la izquierda de la línea x=200.
    y=ax.get_ylim()[1] * 0.90,
    s='Límite deseable\n(200 mg/dl)',
    color='#C51130',
    fontsize=9.5,
    fontweight='bold',
    ha='right',  # Alinea el extremo derecho del texto con x=195.
    va='bottom', # Alinea la parte inferior del texto con la coordenada y.
    clip_on=False # Permite que el texto aparezca fuera del área de los ejes.
)


# LIMPIEZA DE TINTA (TUFT / DESPINE) Y JERARQUÍA TIPOGRÁFICA
# Eliminamos el marco superior y derecho para reducir la carga cognitiva
sns.despine(ax=ax, top=True, right=True)

# Rejilla horizontal tenue exclusivamente en el eje Y para facilitar la lectura de frecuencias
ax.grid(True, axis='y', linestyle=':', alpha=0.35, color='#94A3B8')

# Ajuste de etiquetas de ejes (evitando tecnicismos crudos de base de datos)
ax.set_xlabel('Colesterol sérico (mg/dl)', fontsize=10.5, color='#1E293B', labelpad=8)
ax.set_ylabel('Frecuencia (Nº de pacientes)', fontsize=10.5, color='#1E293B', labelpad=8)
ax.tick_params(colors='#475569', labelsize=9.5)

# Título orientado a la acción (Storytelling): comunica el hallazgo principal
ax.set_title(
    'Distribución de Colesterol Sérico: Sesgo hacia niveles de riesgo (>200 mg/dl)',
    loc='left',
    fontsize=12.5,
    fontweight='bold',
    pad=15,
    color='#0F172A'
)

# RENDERIZADO Y CIERRE DEL GRÁFICO
plt.tight_layout()
plt.show()