"""
Demo Day 2: Observatorio de Cohesión y Convergencia Europea (2000-2024)
Asignatura: Visualización y Análisis de Datos (VAD) - UPM
Autor: Javier

Cuadro de mando interactivo con arquitectura Dash nativa, análisis geoespacial
en Folium, gráficos reactivos en Plotly y reproducción temporal interactiva.
"""

import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import branca.colormap as cm
import folium

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CARGA DE DATOS Y CONFIGURACIÓN INICIAL
# -----------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CSV_PATH = os.path.join(DATA_DIR, 'europe_macro_historical.csv')
GEO_PATH = os.path.join(DATA_DIR, 'europe_geometries.geojson')

df_macro = pd.read_csv(CSV_PATH)
gdf_base = gpd.read_file(GEO_PATH)

# Mapeo descriptivo de métricas para la UI y el mapa
METRIC_CONFIG = {
    'gdp_per_capita': {
        'label': 'PIB per cápita',
        'unit': 'USD',
        'fmt': '${:,.0f}',
        'palette': cm.linear.YlGnBu_09,
        'plot_scale': 'log'
    },
    'life_expectancy': {
        'label': 'Esperanza de vida',
        'unit': 'años',
        'fmt': '{:.1f} años',
        'palette': cm.linear.viridis,
        'plot_scale': 'linear'
    },
    'rd_expenditure': {
        'label': 'Gasto en I+D',
        'unit': '% del PIB',
        'fmt': '{:.2f} %',
        'palette': cm.linear.PuRd_09,
        'plot_scale': 'linear'
    },
    'health_expenditure': {
        'label': 'Gasto en Salud',
        'unit': '% del PIB',
        'fmt': '{:.2f} %',
        'palette': cm.linear.BuPu_09,
        'plot_scale': 'linear'
    },
    'renewable_energy_pct': {
        'label': 'Generación Renovable',
        'unit': '% del mix',
        'fmt': '{:.1f} %',
        'palette': cm.linear.YlGn_09,
        'plot_scale': 'linear'
    },
    'unemployment_rate': {
        'label': 'Tasa de Desempleo',
        'unit': '% activa',
        'fmt': '{:.1f} %',
        'palette': cm.linear.OrRd_09,
        'plot_scale': 'linear'
    },
}

PALETA_REGIONES = {
    'Europa Occidental': '#2563EB',  # Azul
    'Europa del Sur': '#F59E0B',     # Ámbar
    'Europa del Norte': '#10B981',   # Esmeralda
    'Europa del Este': '#8B5CF6',    # Violeta
}

# -----------------------------------------------------------------------------
# 2. INICIALIZACIÓN DE LA APLICACIÓN DASH
# -----------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    title="Observatorio de Cohesión Europea | Demo Day 2",
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True
)
server = app.server

# -----------------------------------------------------------------------------
# 3. COMPONENTES VISUALES DE LA INTERFAZ
# -----------------------------------------------------------------------------

# Panel de Filtros Globales (Shneiderman: Overview first, zoom and filter)
control_panel = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label([
                        html.I(className="fa-solid fa-calendar-days me-2 text-primary"),
                        "Año: ",
                        html.Span("2024", id='year-display-badge', className="badge bg-primary ms-1 fs-6")
                    ], className="fw-bold mb-0 d-flex align-items-center"),
                    dbc.ButtonGroup([
                        dbc.Button(
                            [html.I(className="fa-solid fa-play me-1", id='play-icon'), html.Span("Play", id='play-text')],
                            id='btn-play',
                            color='primary',
                            size='sm',
                            className="shadow-sm fw-bold px-2 py-1"
                        ),
                        dbc.Button(
                            [html.I(className="fa-solid fa-rotate-left me-1"), "2000"],
                            id='btn-reset-year',
                            color='secondary',
                            outline=True,
                            size='sm',
                            className="shadow-sm px-2 py-1",
                            title="Reiniciar al año 2000"
                        ),
                    ], size='sm')
                ], className="d-flex justify-content-between align-items-center mb-1"),
                dcc.Slider(
                    id='year-slider',
                    min=2000,
                    max=2024,
                    step=1,
                    value=2024,
                    marks={y: str(y) for y in range(2000, 2025, 4)},
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                dcc.Interval(
                    id='play-interval',
                    interval=1200,
                    n_intervals=0,
                    disabled=True
                )
            ], md=4, sm=12, className="pe-md-4"),
            dbc.Col([
                html.Label([html.I(className="fa-solid fa-earth-europe me-2 text-primary"), "Macrorregión:"], className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': '🌍 Toda Europa (39 Países)', 'value': 'ALL'}] + [
                        {'label': r, 'value': r} for r in sorted(df_macro['region'].unique())
                    ],
                    value='ALL',
                    clearable=False,
                    className="shadow-sm"
                )
            ], md=3, sm=6),
            dbc.Col([
                html.Label([html.I(className="fa-solid fa-flag me-2 text-primary"), "País Destacado (en cascada):"], className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='country-dropdown',
                    placeholder="Selecciona país...",
                    clearable=False,
                    className="shadow-sm"
                )
            ], md=3, sm=6),
            dbc.Col([
                html.Label([html.I(className="fa-solid fa-sliders me-2 text-primary"), "Métrica del Mapa:"], className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': cfg['label'], 'value': k} for k, cfg in METRIC_CONFIG.items()],
                    value='gdp_per_capita',
                    clearable=False,
                    className="shadow-sm"
                )
            ], md=2, sm=12),
        ], className="align-items-center g-3")
    ]),
    className="border-0 shadow-sm mb-3 bg-light"
)

# Tarjetas superiores de KPIs con metas/referencias obligatorias
kpi_row = dbc.Row(id='kpi-container', className="mb-4 g-3")

# Pestañas principales (Tabs)
tabs = dbc.Tabs([
    dbc.Tab(label="🗺️ Diagnóstico Espacial (Folium)", tab_id="tab-mapa", label_class_name="fw-bold"),
    dbc.Tab(label="📊 Dinámica Temporal & Gapminder (Plotly)", tab_id="tab-plotly", label_class_name="fw-bold"),
], id="tabs-main", active_tab="tab-mapa", className="nav-pills mb-3")

app.layout = dbc.Container([
    control_panel,
    kpi_row,
    tabs,
    html.Div(id='tab-content', className="pb-5"),
    # Footer corporativo
    html.Footer(
        dbc.Container([
            html.Hr(className="my-3 text-muted"),
            dbc.Row([
                dbc.Col("Demo Day 2 · Visualización y Análisis de Datos (VAD) · UPM", className="text-muted small"),
                dbc.Col("Autor: Javier · Arquitectura Dash + Folium + Plotly", className="text-muted small text-end")
            ])
        ], fluid=True),
        className="mt-auto"
    )
], fluid=True, className="px-4 pt-3 bg-white")


# -----------------------------------------------------------------------------
# 4. CALLBACKS REACTIVOS Y EN CASCADA
# -----------------------------------------------------------------------------

# Callback de reproducción temporal automática (Play / Pausa)
@app.callback(
    Output('play-interval', 'disabled'),
    Output('play-icon', 'className'),
    Output('play-text', 'children'),
    Output('btn-play', 'color'),
    Input('btn-play', 'n_clicks'),
    State('play-interval', 'disabled'),
    prevent_initial_call=True
)
def toggle_play(n_clicks, is_disabled):
    if is_disabled:
        return False, "fa-solid fa-pause me-1", "Pausa", "warning"
    else:
        return True, "fa-solid fa-play me-1", "Play", "primary"


# Callback para avanzar o reiniciar el año en la línea temporal
@app.callback(
    Output('year-slider', 'value'),
    Input('play-interval', 'n_intervals'),
    Input('btn-reset-year', 'n_clicks'),
    Input('btn-play', 'n_clicks'),
    State('year-slider', 'value'),
    State('play-interval', 'disabled'),
    prevent_initial_call=True
)
def gestionar_ano(n_intervals, n_reset, n_play, current_year, is_disabled):
    trig = dash.ctx.triggered_id
    if trig == 'btn-reset-year':
        return 2000
    if trig == 'btn-play':
        # Si se inicia la reproducción y ya estamos en 2024, reiniciar a 2000 para empezar desde el inicio
        if is_disabled and (current_year is None or current_year >= 2024):
            return 2000
        return dash.no_update
    if trig == 'play-interval':
        if current_year is None or current_year >= 2024:
            return 2000
        return current_year + 1
    return current_year


# Callback para reflejar el año activo en el badge
@app.callback(
    Output('year-display-badge', 'children'),
    Input('year-slider', 'value')
)
def actualizar_badge_ano(year):
    return str(year)


# Callback 1: Cascada de Región a Países disponibles
@app.callback(
    Output('country-dropdown', 'options'),
    Output('country-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    State('country-dropdown', 'value')
)
def actualizar_paises_en_cascada(region_seleccionada, pais_actual):
    if region_seleccionada == 'ALL':
        df_filtrado = df_macro
    else:
        df_filtrado = df_macro[df_macro['region'] == region_seleccionada]

    paises = sorted(df_filtrado['country_name'].unique())
    opciones = [{'label': p, 'value': p} for p in paises]

    nuevo_pais = pais_actual if pais_actual in paises else (paises[0] if paises else 'España')
    if 'España' in paises and (pais_actual not in paises):
        nuevo_pais = 'España'

    return opciones, nuevo_pais


# Callback 2: Tarjetas Superiores de KPIs dinámicos con referencias
@app.callback(
    Output('kpi-container', 'children'),
    Input('year-slider', 'value'),
    Input('region-dropdown', 'value')
)
def actualizar_kpis(year, region):
    df_y = df_macro[df_macro['year'] == year].copy()
    df_prev = df_macro[df_macro['year'] == max(2000, year - 1)].copy()

    if region != 'ALL':
        df_y = df_y[df_y['region'] == region]
        df_prev = df_prev[df_prev['region'] == region]

    # 1. PIB per cápita medio
    pib_mean = df_y['gdp_per_capita'].mean()
    pib_prev = df_prev['gdp_per_capita'].mean()
    pib_delta = ((pib_mean - pib_prev) / pib_prev) * 100 if pib_prev > 0 else 0

    # 2. Esperanza de vida media
    life_mean = df_y['life_expectancy'].mean()
    life_prev = df_prev['life_expectancy'].mean()
    life_delta = life_mean - life_prev

    # 3. Brecha de Convergencia (Ratio Percentil 90 / Percentil 10)
    p90 = df_y['gdp_per_capita'].quantile(0.90)
    p10 = df_y['gdp_per_capita'].quantile(0.10)
    ratio_brecha = p90 / p10 if p10 > 0 else 1.0

    p90_prev = df_prev['gdp_per_capita'].quantile(0.90)
    p10_prev = df_prev['gdp_per_capita'].quantile(0.10)
    ratio_prev = p90_prev / p10_prev if p10_prev > 0 else ratio_brecha
    brecha_delta = ratio_brecha - ratio_prev

    # 4. Mix Renovable
    ren_mean = df_y['renewable_energy_pct'].mean()
    ren_prev = df_prev['renewable_energy_pct'].mean()
    ren_delta = ren_mean - ren_prev

    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("PIB PER CÁPITA MEDIO", className="text-muted fw-bold small"),
                        html.I(className="fa-solid fa-coins text-primary fs-5")
                    ], className="d-flex justify-content-between align-items-center mb-1"),
                    html.H3(f"${pib_mean:,.0f}", className="fw-bold mb-0 text-dark"),
                    html.Small([
                        html.Span(f"{'▲' if pib_delta >= 0 else '▼'} {abs(pib_delta):.1f}% ",
                                  className="text-success fw-bold" if pib_delta >= 0 else "text-danger fw-bold"),
                        f"vs. año anterior ({year-1})"
                    ], className="text-muted")
                ]), className="border-0 shadow-sm border-start border-4 border-primary h-100"
            ), md=3, sm=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("ESPERANZA DE VIDA MEDIA", className="text-muted fw-bold small"),
                        html.I(className="fa-solid fa-heart-pulse text-success fs-5")
                    ], className="d-flex justify-content-between align-items-center mb-1"),
                    html.H3(f"{life_mean:.1f} años", className="fw-bold mb-0 text-dark"),
                    html.Small([
                        html.Span(f"{'▲' if life_delta >= 0 else '▼'} {abs(life_delta):.2f} años ",
                                  className="text-success fw-bold" if life_delta >= 0 else "text-danger fw-bold"),
                        f"vs. año anterior"
                    ], className="text-muted")
                ]), className="border-0 shadow-sm border-start border-4 border-success h-100"
            ), md=3, sm=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("BRECHA TERRITORIAL (P90/P10)", className="text-muted fw-bold small"),
                        html.I(className="fa-solid fa-scale-unbalanced text-warning fs-5")
                    ], className="d-flex justify-content-between align-items-center mb-1"),
                    html.H3(f"{ratio_brecha:.2f}x", className="fw-bold mb-0 text-dark"),
                    html.Small([
                        html.Span(f"{'▼' if brecha_delta <= 0 else '▲'} {abs(brecha_delta):.2f} pts ",
                                  className="text-success fw-bold" if brecha_delta <= 0 else "text-danger fw-bold"),
                        "Meta cohesión: < 2.0x"
                    ], className="text-muted")
                ]), className="border-0 shadow-sm border-start border-4 border-warning h-100"
            ), md=3, sm=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span("GENERACIÓN RENOVABLE", className="text-muted fw-bold small"),
                        html.I(className="fa-solid fa-leaf text-info fs-5")
                    ], className="d-flex justify-content-between align-items-center mb-1"),
                    html.H3(f"{ren_mean:.1f} %", className="fw-bold mb-0 text-dark"),
                    html.Small([
                        html.Span(f"{'▲' if ren_delta >= 0 else '▼'} {abs(ren_delta):.1f} pp ",
                                  className="text-success fw-bold" if ren_delta >= 0 else "text-danger fw-bold"),
                        "Meta UE 2030: 42.5%"
                    ], className="text-muted")
                ]), className="border-0 shadow-sm border-start border-4 border-info h-100"
            ), md=3, sm=6
        ),
    ]
    return cards


# Callback 3: Conmutador de Pestañas
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs-main', 'active_tab'),
    Input('year-slider', 'value'),
    Input('region-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('metric-dropdown', 'value')
)
def render_tab(active_tab, year, region, country, metric):
    if active_tab == 'tab-mapa':
        return render_tab_mapa(year, region, country, metric)
    elif active_tab == 'tab-plotly':
        return render_tab_plotly(year, region, country, metric)
    return html.Div("Pestaña no encontrada.")


# -----------------------------------------------------------------------------
# RENDER DE PESTAÑA 1: FOLIUM GEOESPACIAL EN IFRAME
# -----------------------------------------------------------------------------
def render_tab_mapa(year, region, country_sel, metric):
    df_y = df_macro[df_macro['year'] == year].copy()
    cfg = METRIC_CONFIG[metric]

    # Unir con geometrías
    gdf_merged = gdf_base.merge(df_y, on='iso_a3', how='left')

    # Configurar escala cromática accesible
    val_min = df_macro[metric].quantile(0.02)
    val_max = df_macro[metric].quantile(0.98)
    colormap = cfg['palette'].scale(val_min, val_max)
    colormap.caption = f"{cfg['label']} ({cfg['unit']}) - Año {year}"

    # Crear mapa de Folium centrado en Europa
    m = folium.Map(
        location=[53.5, 14.0],
        zoom_start=4,
        tiles='OpenStreetMap',
        control_scale=True
    )

    def style_fn(feature):
        props = feature['properties']
        val = props.get(metric)
        c_name = props.get('country_name')

        is_highlighted = (c_name == country_sel)
        fill_col = colormap(val) if (val is not None and not np.isnan(val)) else '#CBD5E1'

        return {
            'fillColor': fill_col,
            'color': '#0F172A' if is_highlighted else '#64748B',
            'weight': 3 if is_highlighted else 1,
            'fillOpacity': 0.85 if is_highlighted else 0.70,
            'dashArray': '4' if is_highlighted else '0'
        }

    # Popups enriquecidos en HTML
    for _, row in gdf_merged.iterrows():
        if pd.isna(row.get('country_name')):
            continue

        c_name = row['country_name']
        val_metric = row.get(metric, 0)
        formatted_val = cfg['fmt'].format(val_metric)

        pib_str = f"${row.get('gdp_per_capita', 0):,.0f}"
        life_str = f"{row.get('life_expectancy', 0):.1f} años"
        unemp_str = f"{row.get('unemployment_rate', 0):.1f}%"
        rd_str = f"{row.get('rd_expenditure', 0):.2f}%"

        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 180px; padding: 4px;">
            <h6 style="margin: 0 0 4px 0; color: #1E293B; font-weight: bold; border-bottom: 2px solid #3B82F6; padding-bottom: 2px;">
                {c_name} <span style="font-size: 0.8em; color: #64748B;">({row.get('region', '')})</span>
            </h6>
            <p style="margin: 4px 0; font-size: 0.95em;">
                <b>{cfg['label']}:</b> <span style="color: #2563EB; font-weight: bold;">{formatted_val}</span>
            </p>
            <div style="font-size: 0.82em; color: #475569; margin-top: 6px;">
                <div>• PIB pc: {pib_str}</div>
                <div>• Esperanza: {life_str}</div>
                <div>• Desempleo: {unemp_str}</div>
                <div>• I+D: {rd_str} del PIB</div>
            </div>
        </div>
        """
        # Añadir marcador de centroide si el país está seleccionado
        if c_name == country_sel and row.geometry:
            centroid = row.geometry.centroid
            folium.Marker(
                location=[centroid.y, centroid.x],
                icon=folium.Icon(color='red', icon='info-sign'),
                popup=folium.Popup(popup_html, max_width=250)
            ).add_to(m)

    geo_data = json.loads(gdf_merged.to_json())
    folium.GeoJson(
        geo_data,
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=['country_name', metric, 'gdp_per_capita', 'life_expectancy'],
            aliases=['País:', f'{cfg["label"]}:', 'PIB pc (USD):', 'Esperanza (años):'],
            localize=True
        )
    ).add_to(m)

    colormap.add_to(m)
    map_html = m.get_root().render()

    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fa-solid fa-map-location-dot me-2 text-primary"),
                    f"Distribución Geoespacial de {cfg['label']} en {year}",
                    html.Span(f" (Filtro activo: {country_sel})", className="badge bg-secondary ms-2")
                ], className="fw-bold bg-white"),
                dbc.CardBody([
                    html.Iframe(
                        srcDoc=map_html,
                        style={'width': '100%', 'height': '580px', 'border': 'none', 'borderRadius': '6px'}
                    )
                ], className="p-1")
            ], className="border-0 shadow-sm")
        ], md=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fa-solid fa-ranking-star me-2 text-primary"),
                    f"Ranking Territorial ({year})"
                ], className="fw-bold bg-white"),
                dbc.CardBody(id='ranking-card-body', children=generar_ranking_card(df_y, metric, country_sel))
            ], className="border-0 shadow-sm mb-3"),
            dbc.Alert([
                html.I(className="fa-solid fa-lightbulb me-2"),
                html.B("Lectura analítica: "),
                "Los países con mayor gasto en I+D y transición energética superan en más de un 100% el PIB per cápita promedio del Este europeo. ",
                "Haz clic en cualquier país en el mapa para inspeccionar sus métricas detalladas."
            ], color="info", className="border-0 shadow-sm small")
        ], md=4)
    ])


def generar_ranking_card(df_y, metric, country_sel):
    cfg = METRIC_CONFIG[metric]
    df_sorted = df_y.sort_values(by=metric, ascending=False).reset_index(drop=True)

    items = []
    top_5 = df_sorted.head(5)
    bottom_5 = df_sorted.tail(5)

    items.append(html.P("Top 5 Países Líderes:", className="fw-bold text-success small mb-1"))
    for idx, row in top_5.iterrows():
        is_sel = (row['country_name'] == country_sel)
        items.append(
            html.Div([
                html.Span(f"{idx+1}. {row['country_name']}", className="fw-bold" if is_sel else ""),
                html.Span(cfg['fmt'].format(row[metric]), className="badge bg-light text-dark border")
            ], className=f"d-flex justify-content-between py-1 border-bottom {'bg-warning-subtle px-1 rounded' if is_sel else ''}")
        )

    items.append(html.P("5 Países con Menor Valor:", className="fw-bold text-danger small mt-3 mb-1"))
    for idx, row in bottom_5.iterrows():
        is_sel = (row['country_name'] == country_sel)
        items.append(
            html.Div([
                html.Span(f"{len(df_sorted)-4+idx}. {row['country_name']}", className="fw-bold" if is_sel else ""),
                html.Span(cfg['fmt'].format(row[metric]), className="badge bg-light text-dark border")
            ], className=f"d-flex justify-content-between py-1 border-bottom {'bg-warning-subtle px-1 rounded' if is_sel else ''}")
        )
    return items


# -----------------------------------------------------------------------------
# RENDER DE PESTAÑA 2: GRÁFICOS PLOTLY ENLAZADOS & GAPMINDER
# -----------------------------------------------------------------------------
def render_tab_plotly(year, region, country_sel, metric):
    df_y = df_macro[df_macro['year'] == year].copy()
    if region != 'ALL':
        df_y = df_y[df_y['region'] == region]

    # Gráfico 1: Dispersión Multidimensional Gapminder (PIB vs Esperanza de vida)
    fig_scatter = px.scatter(
        df_y,
        x="gdp_per_capita",
        y="life_expectancy",
        size="population",
        color="region",
        hover_name="country_name",
        color_discrete_map=PALETA_REGIONES,
        log_x=True,
        size_max=45,
        labels={
            "gdp_per_capita": "PIB per cápita (USD, escala log)",
            "life_expectancy": "Esperanza de vida (años)",
            "region": "Macrorregión",
            "population": "Población"
        },
        title=f"<b>Relación PIB per cápita vs. Esperanza de Vida ({year})</b>"
    )

    # Destacar país seleccionado
    df_sel = df_y[df_y['country_name'] == country_sel]
    if not df_sel.empty:
        fig_scatter.add_trace(
            go.Scatter(
                x=df_sel['gdp_per_capita'],
                y=df_sel['life_expectancy'],
                mode='markers+text',
                marker=dict(size=22, color='rgba(0,0,0,0)', line=dict(color='black', width=3)),
                text=[f"📍 {country_sel}"],
                textposition="top center",
                showlegend=False,
                name=country_sel
            )
        )

    # Límites estables para evitar animaciones saltarinas (Evitar Muro de los Horrores)
    fig_scatter.update_layout(
        xaxis=dict(range=[2.5, 5.3], gridcolor='#E2E8F0'),
        yaxis=dict(range=[65, 87], gridcolor='#E2E8F0'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="sans-serif", color="#1E293B"),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Gráfico 2: Serie Temporal con RangeSlider y RangeSelector del País Seleccionado
    df_hist_country = df_macro[df_macro['country_name'] == country_sel].sort_values('year')
    df_hist_eu = df_macro.groupby('year')[metric].mean().reset_index()

    cfg = METRIC_CONFIG[metric]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_hist_eu['year'],
        y=df_hist_eu[metric],
        mode='lines',
        name='Media Europea',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    fig_line.add_trace(go.Scatter(
        x=df_hist_country['year'],
        y=df_hist_country[metric],
        mode='lines+markers',
        name=country_sel,
        line=dict(color='#2563EB', width=3),
        marker=dict(size=6)
    ))

    # Punto del año actual
    curr_point = df_hist_country[df_hist_country['year'] == year]
    if not curr_point.empty:
        fig_line.add_trace(go.Scatter(
            x=curr_point['year'],
            y=curr_point[metric],
            mode='markers+text',
            name='Año seleccionado',
            marker=dict(size=12, color='#EF4444'),
            text=[f"{cfg['fmt'].format(curr_point[metric].values[0])}"],
            textposition="top center",
            showlegend=False
        ))

    fig_line.update_layout(
        title=f"<b>Evolución Histórica de {cfg['label']} (2000–2024): {country_sel} vs. Media UE</b>",
        xaxis=dict(
            title="Año",
            rangeslider=dict(visible=True),
            gridcolor='#E2E8F0'
        ),
        yaxis=dict(title=f"{cfg['label']} ({cfg['unit']})", gridcolor='#E2E8F0'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="sans-serif", color="#1E293B"),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure=fig_scatter, config={'displayModeBar': False})])
            ], className="border-0 shadow-sm")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure=fig_line, config={'displayModeBar': False})])
            ], className="border-0 shadow-sm")
        ], md=6)
    ])





# -----------------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Ejecución directa del servidor Flask embebido en Dash
    app.run(debug=True, host='0.0.0.0', port=8050)
