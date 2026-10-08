"""
Descarga y procesamiento de datos macroeconómicos históricos (2000-2024)
para el Observatorio de Cohesión y Convergencia Europea (Demo Day 2).
Fuente: Banco Mundial Open Data API & Natural Earth Geometries.
"""

import json
import time
import urllib.request
import pandas as pd
import geopandas as gpd

REGION_MAPPING = {
    'ESP': ('España', 'Europa del Sur'),
    'PRT': ('Portugal', 'Europa del Sur'),
    'ITA': ('Italia', 'Europa del Sur'),
    'GRC': ('Grecia', 'Europa del Sur'),
    'FRA': ('Francia', 'Europa Occidental'),
    'DEU': ('Alemania', 'Europa Occidental'),
    'BEL': ('Bélgica', 'Europa Occidental'),
    'NLD': ('Países Bajos', 'Europa Occidental'),
    'LUX': ('Luxemburgo', 'Europa Occidental'),
    'CHE': ('Suiza', 'Europa Occidental'),
    'AUT': ('Austria', 'Europa Occidental'),
    'GBR': ('Reino Unido', 'Europa Occidental'),
    'IRL': ('Irlanda', 'Europa Occidental'),
    'NOR': ('Noruega', 'Europa del Norte'),
    'SWE': ('Suecia', 'Europa del Norte'),
    'DNK': ('Dinamarca', 'Europa del Norte'),
    'FIN': ('Finlandia', 'Europa del Norte'),
    'ISL': ('Islandia', 'Europa del Norte'),
    'EST': ('Estonia', 'Europa del Norte'),
    'LVA': ('Letonia', 'Europa del Norte'),
    'LTU': ('Lituania', 'Europa del Norte'),
    'POL': ('Polonia', 'Europa del Este'),
    'CZE': ('Chequia', 'Europa del Este'),
    'SVK': ('Eslovaquia', 'Europa del Este'),
    'HUN': ('Hungría', 'Europa del Este'),
    'ROU': ('Rumanía', 'Europa del Este'),
    'BGR': ('Bulgaria', 'Europa del Este'),
    'HRV': ('Croacia', 'Europa del Este'),
    'SVN': ('Eslovenia', 'Europa del Este'),
    'SRB': ('Serbia', 'Europa del Este'),
    'BIH': ('Bosnia y Herz.', 'Europa del Este'),
    'MNE': ('Montenegro', 'Europa del Este'),
    'MKD': ('Macedonia del N.', 'Europa del Este'),
    'ALB': ('Albania', 'Europa del Este'),
    'XKX': ('Kosovo', 'Europa del Este'),
    'MDA': ('Moldavia', 'Europa del Este'),
    'UKR': ('Ucrania', 'Europa del Este'),
    'BLR': ('Bielorrusia', 'Europa del Este'),
    'RUS': ('Rusia', 'Europa del Este'),
}

INDICATORS = {
    'NY.GDP.PCAP.CD': 'gdp_per_capita',       # PIB per cápita (USD corriente)
    'SP.DYN.LE00.IN': 'life_expectancy',       # Esperanza de vida al nacer (años)
    'SP.POP.TOTL': 'population',               # Población total
    'SL.UEM.TOTL.ZS': 'unemployment_rate',     # Tasa de desempleo (% activa)
    'GB.XPD.RSDV.GD.ZS': 'rd_expenditure',     # Gasto en I+D (% del PIB)
    'SH.XPD.CHEX.GD.ZS': 'health_expenditure', # Gasto en salud (% del PIB)
    'EG.ELC.RNEW.ZS': 'renewable_energy_pct',  # Generación renovable (% mix)
    'FP.CPI.TOTL.ZG': 'inflation_rate',        # Tasa de inflación anual (%)
    'NE.EXP.GNFS.ZS': 'exports_pct_gdp',       # Exportaciones (% del PIB)
}


def descargar_indicador(indicator_code, indicator_name, countries_str, start_year=2000, end_year=2024):
    """Descarga un indicador desde la API del Banco Mundial para el conjunto de países."""
    url = f"http://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator_code}?date={start_year}:{end_year}&format=json&per_page=3000"
    print(f"Descargando {indicator_name} ({indicator_code})...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1 and data[1]:
                records = []
                for entry in data[1]:
                    c_code = entry.get('countryiso3code')
                    year = int(entry.get('date'))
                    val = entry.get('value')
                    records.append({'iso_a3': c_code, 'year': year, indicator_name: val})
                return pd.DataFrame(records)
            else:
                print(f"Aviso: Respuesta vacía para {indicator_name}")
    except Exception as e:
        print(f"Error al descargar {indicator_name}: {e}")
    return pd.DataFrame()


def main():
    countries = list(REGION_MAPPING.keys())
    countries_str = ";".join(countries)
    start_year, end_year = 2000, 2024

    df_base = None

    for ind_code, ind_name in INDICATORS.items():
        df_ind = descargar_indicador(ind_code, ind_name, countries_str, start_year, end_year)
        if not df_ind.empty:
            if df_base is None:
                df_base = df_ind
            else:
                df_base = pd.merge(df_base, df_ind, on=['iso_a3', 'year'], how='outer')
        time.sleep(0.4)

    if df_base is None or df_base.empty:
        print("Error: No se pudieron obtener datos.")
        return

    # Mapear nombres y regiones
    df_base['country_name'] = df_base['iso_a3'].map(lambda x: REGION_MAPPING.get(x, (x, 'Otros'))[0])
    df_base['region'] = df_base['iso_a3'].map(lambda x: REGION_MAPPING.get(x, (x, 'Otros'))[1])

    # Ordenar por país y año
    df_base = df_base.sort_values(by=['iso_a3', 'year']).reset_index(drop=True)

    # Identificar columnas descargadas con éxito
    numeric_cols = [c for c in INDICATORS.values() if c in df_base.columns]

    # Imputación / Forward-fill & Backward-fill por país para evitar huecos en series históricas
    for col in numeric_cols:
        df_base[col] = df_base.groupby('iso_a3')[col].transform(lambda s: s.ffill().bfill())

    # Rellenar valores que aún pudieran ser NaN con la mediana regional de ese año
    for col in numeric_cols:
        df_base[col] = df_base.groupby(['region', 'year'])[col].transform(lambda s: s.fillna(s.median()))
        # Si aún queda algo, mediana global
        df_base[col] = df_base[col].fillna(df_base[col].median())

    # Métricas derivadas útiles para la visualización y KPIs
    df_base['pop_millions'] = df_base['population'] / 1e6
    df_base['gdp_total_billions'] = (df_base['gdp_per_capita'] * df_base['population']) / 1e9
    df_base['gdp_per_capita_relative'] = (df_base['gdp_per_capita'] / df_base.groupby('year')['gdp_per_capita'].transform('mean')) * 100

    # Guardar CSV consolidado
    csv_path = 'DemoDay2/data/europe_macro_historical.csv'
    df_base.to_csv(csv_path, index=False)
    print(f"Dataset guardado con éxito en: {csv_path}")
    print(f"Filas: {len(df_base)}, Columnas: {df_base.columns.tolist()}")

    # Ahora cargar el GeoJSON de DemoDay1 y sincronizarlo
    try:
        gdf_geo = gpd.read_file('DemoDay1/europe.geojson')
        gdf_geo.loc[gdf_geo['name'] == 'Kosovo', 'iso_a3'] = 'XKX'
        gdf_geo = gdf_geo[gdf_geo['iso_a3'].isin(countries)].copy()
        
        geo_path = 'DemoDay2/data/europe_geometries.geojson'
        gdf_geo.to_file(geo_path, driver='GeoJSON')
        print(f"Geometrías guardadas en: {geo_path}")
    except Exception as e:
        print(f"Error procesando geometrías: {e}")


if __name__ == '__main__':
    main()
