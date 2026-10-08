"""
Generación y exportación de gráficos en alta resolución (300 DPI y vectoriales .pdf)
para la entrega del Demo Day 2 (Rúbrica oficial UPM - VAD).
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd

# Configuración estética ejecutiva y académica
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'figuras')
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_DIR, 'europe_macro_historical.csv'))
gdf = gpd.read_file(os.path.join(DATA_DIR, 'europe_geometries.geojson'))

PALETA_REGIONES = {
    'Europa Occidental': '#2563EB',
    'Europa del Sur': '#F59E0B',
    'Europa del Norte': '#10B981',
    'Europa del Este': '#8B5CF6',
}

# -----------------------------------------------------------------------------
# FIGURA 1: MAPA COROPLÉTICO ESPACIAL (PIB PER CÁPITA 2024)
# -----------------------------------------------------------------------------
df_2024 = df[df['year'] == 2024]
gdf_merged = gdf.merge(df_2024, on='iso_a3', how='left')

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
gdf_merged.plot(
    column='gdp_per_capita',
    cmap='YlGnBu',
    legend=True,
    legend_kwds={
        'label': "PIB per cápita (USD - 2024)",
        'orientation': "horizontal",
        'shrink': 0.6,
        'pad': 0.05
    },
    edgecolor='#475569',
    linewidth=0.6,
    missing_kwds={'color': '#E2E8F0', 'label': 'Sin datos'},
    ax=ax
)
ax.set_xlim(-25, 45)
ax.set_ylim(34, 72)
ax.set_title("Figura 1: Diagnóstico Geoespacial de Cohesión Europea (PIB pc 2024)", fontsize=14, fontweight='bold', pad=15)
ax.axis('off')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_1_mapa_convergencia.png'), dpi=300)
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_1_mapa_convergencia.pdf'))
plt.close(fig)
print("Figura 1 guardada.")

# -----------------------------------------------------------------------------
# FIGURA 2: DISPERSIÓN MULTIDIMENSIONAL GAPMINDER (PIB VS LONGEVIDAD)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
for reg, group in df_2024.groupby('region'):
    ax.scatter(
        group['gdp_per_capita'],
        group['life_expectancy'],
        s=group['population'] / 350000,
        color=PALETA_REGIONES.get(reg, '#64748B'),
        alpha=0.75,
        edgecolors='white',
        linewidth=1.2,
        label=reg
    )

# Anotaciones de países clave
paises_clave = ['Luxemburgo', 'Alemania', 'España', 'Polonia', 'Bulgaria', 'Noruega']
for _, row in df_2024[df_2024['country_name'].isin(paises_clave)].iterrows():
    ax.annotate(
        row['country_name'],
        (row['gdp_per_capita'], row['life_expectancy']),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold',
        color='#0F172A'
    )

ax.set_xscale('log')
ax.set_title("Figura 2: Dinámica Multivariante Gapminder (PIB pc vs. Esperanza de Vida, 2024)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("PIB per cápita en USD (Escala logarítmica)", fontsize=11, fontweight='bold')
ax.set_ylabel("Esperanza de vida al nacer (Años)", fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
ax.legend(title="Macrorregión", frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_2_dinamica_gapminder.png'), dpi=300)
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_2_dinamica_gapminder.pdf'))
plt.close(fig)
print("Figura 2 guardada.")

# -----------------------------------------------------------------------------
# FIGURA 3: EVOLUCIÓN HISTÓRICA Y CONVERGENCIA MACRORREGIONAL (2000-2024)
# -----------------------------------------------------------------------------
df_evo = df.groupby(['year', 'region'])['gdp_per_capita'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
for reg, grp in df_evo.groupby('region'):
    ax.plot(
        grp['year'],
        grp['gdp_per_capita'],
        marker='o',
        markersize=4,
        linewidth=2.5,
        color=PALETA_REGIONES.get(reg, '#64748B'),
        label=reg
    )

ax.set_title("Figura 3: Convergencia de PIB per Cápita por Macrorregiones (2000–2024)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("Año", fontsize=11, fontweight='bold')
ax.set_ylabel("PIB per cápita medio (USD)", fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
ax.legend(title="Macrorregión", frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_3_evolucion_historica.png'), dpi=300)
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_3_evolucion_historica.pdf'))
plt.close(fig)
print("Figura 3 guardada.")

# -----------------------------------------------------------------------------
# FIGURA 4: DISTRIBUCIÓN Y BRECHA TERRITORIAL POR MACRORREGIÓN
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
sns.boxplot(
    data=df_2024,
    x='region',
    y='gdp_per_capita',
    palette=PALETA_REGIONES,
    ax=ax,
    boxprops=dict(alpha=0.8)
)
sns.stripplot(
    data=df_2024,
    x='region',
    y='gdp_per_capita',
    color='#0F172A',
    alpha=0.6,
    jitter=0.2,
    size=5,
    ax=ax
)
ax.set_title("Figura 4: Distribución y Dispersión Territorial de Ingresos (2024)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("Macrorregión Europea", fontsize=11, fontweight='bold')
ax.set_ylabel("PIB per cápita (USD)", fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5, axis='y', color='#CBD5E1')
plt.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_4_ranking_macrorregional.png'), dpi=300)
fig.savefig(os.path.join(OUTPUT_DIR, 'figura_4_ranking_macrorregional.pdf'))
plt.close(fig)
print("Figura 4 guardada.")

print("Todas las figuras generadas con éxito en alta resolución (PNG 300 DPI y Vectorial PDF).")
