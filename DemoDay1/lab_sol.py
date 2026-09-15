"""
Demo Day 1: El Arte de los Datos Estáticos
Proyecto: La Brecha de Prosperidad Europea: Asimetrías Territoriales y Socioeconómicas
Asignatura: Visualización y Análisis de Datos (VAD) - UPM
Autor: Javier
Metodología: Storytelling with Data (Cole Nussbaumer Knaflic), Edward Tufte y Atributos Preatencionales
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


def configurar_estilo():
    """Configura el estilo corporativo limpio (#FAFAFA) y sin ruido."""
    os.makedirs('figuras', exist_ok=True)
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.facecolor'] = '#FAFAFA'
    plt.rcParams['axes.facecolor'] = '#FAFAFA'
    plt.rcParams['axes.edgecolor'] = '#94A3B8'
    plt.rcParams['text.color'] = '#1E293B'
    plt.rcParams['axes.labelcolor'] = '#1E293B'
    plt.rcParams['xtick.color'] = '#475569'
    plt.rcParams['ytick.color'] = '#475569'


def cargar_y_procesar_datos(ruta_geojson='europe.geojson'):
    """Carga y calcula las métricas macroeconómicas derivadas."""
    gdf = gpd.read_file(ruta_geojson)
    gdf['gdp_total_usd'] = gdf['gdp_md_est'] * 1e6
    gdf['pop_millions'] = gdf['pop_est'] / 1e6
    gdf['gdp_billions'] = gdf['gdp_md_est'] / 1e3
    gdf['gdp_per_capita'] = gdf['gdp_total_usd'] / gdf['pop_est']
    return gdf


def generar_grafico_1_mapa(gdf):
    """Gráfico 1: Mapa coroplético de Europa con decluttering y anotaciones directas."""
    fig, ax = plt.subplots(figsize=(11, 8.5), facecolor='#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    fig.subplots_adjust(top=0.88, bottom=0.1)

    # Trazar mapa: Rusia se pinta en gris neutro de fondo para no distorsionar el continente
    paises_mapa = gdf[gdf['name'] != 'Russia'].copy()
    gdf[gdf['name'] == 'Russia'].plot(ax=ax, color='#E2E8F0', edgecolor='#CBD5E1', linewidth=0.5)

    paises_mapa.plot(
        column='gdp_per_capita',
        ax=ax,
        cmap='YlGnBu',
        edgecolor='#FFFFFF',
        linewidth=0.6,
        legend=True,
        legend_kwds={
            'label': 'PIB per Cápita estimado (USD por habitante)',
            'orientation': 'horizontal',
            'shrink': 0.55,
            'pad': 0.04,
            'format': ticker.FuncFormatter(lambda x, pos: f'${int(x/1000)}k')
        }
    )

    ax.set_xlim(-25, 40)
    ax.set_ylim(34, 72)
    ax.set_axis_off()

    # Título y subtítulo limpios en coordenadas de figura
    fig.text(0.06, 0.95, 'La Fractura Territorial de Europa: Concentración de Riqueza en el Eje Central-Nórdico',
             fontsize=13.5, fontweight='bold', color='#0F172A', ha='left')
    fig.text(0.06, 0.92, 'Distribución geográfica del PIB per cápita en 39 naciones. Destaca la brecha entre el bloque occidental y la periferia oriental.',
             fontsize=9.5, color='#64748B', ha='left')

    # Anotaciones estratégicas
    ax.annotate(
        'Eje de máxima prosperidad\n(Suiza, Luxemburgo, Nórdicos >$60k)',
        xy=(6, 50),
        xytext=(-20, 62),
        arrowprops=dict(facecolor='#0284C7', edgecolor='#0284C7', arrowstyle='->', lw=1.5),
        fontsize=9.5,
        fontweight='bold',
        color='#0284C7',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=0.92)
    )

    ax.annotate(
        'Franja de vulnerabilidad oriental\n(Balcanes y Ucrania <$10k)',
        xy=(26, 47),
        xytext=(23, 37.5),
        arrowprops=dict(facecolor='#D92121', edgecolor='#D92121', arrowstyle='->', lw=1.5),
        fontsize=9.5,
        fontweight='bold',
        color='#D92121',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=0.92)
    )

    plt.savefig('figuras/grafico_1_mapa_europa.png', dpi=300, bbox_inches='tight')
    plt.savefig('figuras/grafico_1_mapa_europa.pdf', bbox_inches='tight')
    plt.close()
    print('Gráfico 1 generado exitosamente.')


def generar_grafico_2_extremos(gdf):
    """Gráfico 2: Barras horizontales Top 5 vs Bottom 5 con color preatencional."""
    top5 = gdf.nlargest(5, 'gdp_per_capita').sort_values('gdp_per_capita', ascending=True)
    bottom5 = gdf.nsmallest(5, 'gdp_per_capita').sort_values('gdp_per_capita', ascending=True)

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(10, 6.5), facecolor='#FAFAFA',
        gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.4}
    )
    fig.subplots_adjust(top=0.86)

    # Top 5
    colores_top = ['#93C5FD', '#93C5FD', '#93C5FD', '#93C5FD', '#00629B']
    bars_top = ax_top.barh(top5['name'], top5['gdp_per_capita'] / 1000, color=colores_top, height=0.58)
    for bar in bars_top:
        w = bar.get_width()
        ax_top.text(w + 1.8, bar.get_y() + bar.get_height() / 2, f'${w:,.1f}k',
                    va='center', ha='left', fontsize=9.5, fontweight='bold', color='#1E293B')
    sns.despine(ax=ax_top, top=True, right=True, bottom=True, left=True)
    ax_top.xaxis.set_visible(False)
    ax_top.tick_params(axis='y', length=0, labelsize=10.5, colors='#1E293B')
    ax_top.set_xlim(0, 135)
    ax_top.set_title('TOP 5 MÁS PRÓSPEROS (Líder continental: Luxemburgo)', loc='left', fontsize=10.5, fontweight='bold', color='#00629B', pad=6)

    # Bottom 5
    colores_bot = ['#D92121', '#FCA5A5', '#FCA5A5', '#FCA5A5', '#FCA5A5']
    bars_bot = ax_bot.barh(bottom5['name'], bottom5['gdp_per_capita'] / 1000, color=colores_bot, height=0.58)
    for bar in bars_bot:
        w = bar.get_width()
        ax_bot.text(w + 1.8, bar.get_y() + bar.get_height() / 2, f'${w:,.1f}k',
                    va='center', ha='left', fontsize=9.5, fontweight='bold', color='#1E293B')
    sns.despine(ax=ax_bot, top=True, right=True, bottom=True, left=True)
    ax_bot.xaxis.set_visible(False)
    ax_bot.tick_params(axis='y', length=0, labelsize=10.5, colors='#1E293B')
    ax_bot.set_xlim(0, 135)
    ax_bot.set_title('BOTTOM 5 MÁS VULNERABLES (Mínimo continental: Ucrania)', loc='left', fontsize=10.5, fontweight='bold', color='#D92121', pad=6)

    fig.text(0.06, 0.95, 'Abismo de Ingresos en Europa: Top 5 frente al Bottom 5',
             fontsize=13.5, fontweight='bold', color='#0F172A', ha='left')
    fig.text(0.06, 0.91, 'PIB per cápita anual (miles de USD). La renta en Luxemburgo multiplica por 33 a la de Ucrania (Brecha extrema de 33 a 1).',
             fontsize=9.5, color='#64748B', ha='left')

    plt.savefig('figuras/grafico_2_brecha_extremos.png', dpi=300, bbox_inches='tight')
    plt.savefig('figuras/grafico_2_brecha_extremos.pdf', bbox_inches='tight')
    plt.close()
    print('Gráfico 2 generado exitosamente.')


def generar_grafico_3_dispersion(gdf):
    """Gráfico 3: Dispersión bivariada (Población vs PIB total) con anotaciones directas."""
    fig, ax = plt.subplots(figsize=(10.5, 6.5), facecolor='#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    fig.subplots_adjust(top=0.88)

    scatter = ax.scatter(
        gdf['pop_millions'],
        gdf['gdp_billions'],
        c=gdf['gdp_per_capita'] / 1000,
        cmap='Blues',
        s=140,
        alpha=0.85,
        edgecolors='#334155',
        linewidth=0.8
    )

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.75, pad=0.03)
    cbar.set_label('PIB per Cápita ($k USD)', fontsize=9.5, color='#1E293B')
    cbar.outline.set_visible(False)

    etiquetas_destacadas = {
        'Germany': (4, 30),
        'United Kingdom': (4, -40),
        'France': (-28, 25),
        'Italy': (4, 25),
        'Russia': (-40, 25),
        'Luxembourg': (3, 70),
        'Switzerland': (4, 30),
        'Ukraine': (3, -40),
        'Spain': (4, -30)
    }

    for _, row in gdf.iterrows():
        if row['name'] in etiquetas_destacadas:
            dx, dy = etiquetas_destacadas[row['name']]
            ax.annotate(
                row['name'],
                xy=(row['pop_millions'], row['gdp_billions']),
                xytext=(row['pop_millions'] + dx, row['gdp_billions'] + dy),
                fontsize=8.5,
                fontweight='bold',
                color='#0F172A',
                arrowprops=dict(arrowstyle='->', color='#94A3B8', lw=0.8)
            )

    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    sns.despine(ax=ax, top=True, right=True)

    ax.set_xlabel('Población Nacional (Millones de habitantes)', fontsize=10, labelpad=10)
    ax.set_ylabel('PIB Nacional Estimado (Miles de Millones USD)', fontsize=10, labelpad=10)

    fig.text(0.06, 0.95, 'Volumen Nacional vs. Productividad per Cápita: La Disociación Económica',
             fontsize=13.5, fontweight='bold', color='#0F172A', ha='left')
    fig.text(0.06, 0.91, 'Relación entre tamaño demográfico y masa económica. Los líderes en bienestar (Suiza, Luxemburgo) no son gigantes poblacionales.',
             fontsize=9.5, color='#64748B', ha='left')

    plt.savefig('figuras/grafico_3_dispersion_pib_poblacion.png', dpi=300, bbox_inches='tight')
    plt.savefig('figuras/grafico_3_dispersion_pib_poblacion.pdf', bbox_inches='tight')
    plt.close()
    print('Gráfico 3 generado exitosamente.')


def generar_grafico_4_distribucion(gdf):
    """Gráfico 4: Histograma + KDE y demostración de la falacia de la media."""
    media_pib_pc = gdf['gdp_per_capita'].mean()
    mediana_pib_pc = gdf['gdp_per_capita'].median()

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    fig.subplots_adjust(top=0.87)

    sns.histplot(
        gdf['gdp_per_capita'] / 1000,
        kde=True,
        bins=14,
        color='#0284C7',
        alpha=0.3,
        edgecolor='#0284C7',
        line_kws={'linewidth': 2.2, 'color': '#0369A1'},
        ax=ax
    )

    ax.axvline(mediana_pib_pc / 1000, color='#D92121', linestyle='--', linewidth=2)
    ax.axvline(media_pib_pc / 1000, color='#00629B', linestyle='-', linewidth=2)

    ax.text(
        mediana_pib_pc / 1000 - 1.5, 7.5,
        f'Mediana\n${mediana_pib_pc/1000:,.1f}k',
        color='#D92121',
        fontsize=9.5,
        fontweight='bold',
        ha='right'
    )
    ax.text(
        media_pib_pc / 1000 + 1.5, 7.5,
        f'Media inflada\n${media_pib_pc/1000:,.1f}k',
        color='#00629B',
        fontsize=9.5,
        fontweight='bold',
        ha='left'
    )

    porcentaje_bajo_media = (gdf['gdp_per_capita'] < media_pib_pc).mean() * 100
    ax.text(
        65, 4.5,
        f'Asimetría positiva notable (Right-Skewed):\nEl {porcentaje_bajo_media:.0f}% de los países europeos\ntienen un PIB per cápita inferior a la media.\nUnos pocos hubs (Luxemburgo, Suiza)\nsesgan el promedio al alza.',
        fontsize=9.5,
        color='#475569',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#F1F5F9', edgecolor='#CBD5E1')
    )

    sns.despine(ax=ax, top=True, right=True)
    ax.set_xlabel('PIB per Cápita ($k USD)', fontsize=10, labelpad=8)
    ax.set_ylabel('Frecuencia (Número de naciones)', fontsize=10, labelpad=8)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    fig.text(0.06, 0.95, 'La Falacia de la Media Europea: Distribución Sesgada del Bienestar',
             fontsize=13.5, fontweight='bold', color='#0F172A', ha='left')
    fig.text(0.06, 0.91, f'Comparativa de medidas de tendencia central. La media (${media_pib_pc/1000:,.1f}k) distorsiona la realidad frente a la mediana (${mediana_pib_pc/1000:,.1f}k).',
             fontsize=9.5, color='#64748B', ha='left')

    plt.savefig('figuras/grafico_4_distribucion_sesgo.png', dpi=300, bbox_inches='tight')
    plt.savefig('figuras/grafico_4_distribucion_sesgo.pdf', bbox_inches='tight')
    plt.close()
    print('Gráfico 4 generado exitosamente.')


def main():
    print('Iniciando pipeline de visualización estática para Demo Day 1...')
    configurar_estilo()
    gdf = cargar_y_procesar_datos('europe.geojson')
    print(f'Datos cargados correctamente: {len(gdf)} países.')
    generar_grafico_1_mapa(gdf)
    generar_grafico_2_extremos(gdf)
    generar_grafico_3_dispersion(gdf)
    generar_grafico_4_distribucion(gdf)
    print('Todas las visualizaciones han sido exportadas a /figuras en alta resolución (PNG a 300 DPI y PDF).')


if __name__ == '__main__':
    main()
