import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2563EB"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(48, 804, "VAD · TEMA 3 (VISUALIZACIÓN DINÁMICA E INTERACTIVA)")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(547, 804, "Demo Day 2: Guion de Defensa Oral (5 min) — Javier Ferreño")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(48, 798, 547, 798)

        # Footer
        text = f"Página {self._pageNumber} de {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(547, 30, text)
        self.drawString(48, 30, "Observatorio de Cohesión Europea · UPM · Despliegue: https://vad-u2iv.onrender.com/")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(48, 40, 547, 40)
        self.restoreState()

def generar_pdf():
    output_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(output_dir, "guion_defensa_5_minutos.pdf")

    # A4: 595.27 x 841.89 pt. Márgenes de 48 pt dejan ancho útil = 499 pt.
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Colores corporativos y temáticos
    C_NAVY = colors.HexColor("#0F172A")
    C_BLUE = colors.HexColor("#2563EB")
    C_BLUE_LIGHT = colors.HexColor("#EFF6FF")
    C_GREEN = colors.HexColor("#059669")
    C_GREEN_LIGHT = colors.HexColor("#ECFDF5")
    C_AMBER = colors.HexColor("#D97706")
    C_AMBER_LIGHT = colors.HexColor("#FFFBEB")
    C_PURPLE = colors.HexColor("#7C3AED")
    C_PURPLE_LIGHT = colors.HexColor("#F5F3FF")
    C_MUTED = colors.HexColor("#475569")
    C_BORDER = colors.HexColor("#CBD5E1")

    # Tipografías y jerarquía
    style_title = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=C_NAVY, spaceAfter=2
    )
    style_subtitle = ParagraphStyle(
        'DocSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=C_BLUE, spaceAfter=6
    )
    style_meta = ParagraphStyle(
        'Meta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=C_MUTED
    )
    style_sec_heading = ParagraphStyle(
        'SecHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=C_NAVY, spaceBefore=8, spaceAfter=4
    )
    style_badge = ParagraphStyle(
        'Badge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=11.5,
        textColor=C_BLUE
    )
    style_action = ParagraphStyle(
        'Action', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10.5,
        textColor=colors.HexColor("#92400E")
    )
    style_speech = ParagraphStyle(
        'Speech', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=C_NAVY
    )
    style_table_header = ParagraphStyle(
        'TblHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10.5,
        textColor=C_NAVY
    )
    style_table_cell = ParagraphStyle(
        'TblCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.8, leading=10.5,
        textColor=C_MUTED
    )
    style_tip = ParagraphStyle(
        'Tip', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=colors.HexColor("#065F46")
    )

    story = []

    # =========================================================================
    # PÁGINA 1: CABECERA, HILO CONDUCTOR Y TECNOLOGÍAS DEL TEMA 3
    # =========================================================================
    story.append(Paragraph("Observatorio de Cohesión y Convergencia Europea", style_title))
    story.append(Paragraph("Guion de Defensa Oral (5 Minutos) &nbsp;|&nbsp; Demo Day 2 (70% Evaluación)", style_subtitle))
    
    meta_text = "<b>Autor:</b> Javier Ferreño &nbsp;|&nbsp; <b>Asignatura:</b> Visualización y Análisis de Datos (VAD) · <b>UPM</b><br/>" \
                "<b>Ejecución Local:</b> <code>pip install -r requirements.txt &amp;&amp; python lab_sol.py</code> (http://localhost:8050)<br/>" \
                "<b>Despliegue Público Cloud:</b> <font color='#2563EB'><u>https://vad-u2iv.onrender.com/</u></font> (Docker en Render con SSL)"
    story.append(Paragraph(meta_text, style_meta))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=3, spaceAfter=6))

    # 1. El Hilo Conductor
    story.append(Paragraph("1. El Hilo Conductor: De la Foto Estática a la Película Interactiva", style_sec_heading))
    narrative_p = Paragraph(
        "<b>• Demo Day 1 (La Fotografía Estática):</b> Demostramos la <i>falacia de la media continental</i> "
        "(el 64% de los países vivían por debajo de la media europea inflada por outliers como Luxemburgo y Suiza) "
        "y evidenciamos una fractura de más de 30 a 1 entre extremos.<br/>"
        "<b>• Demo Day 2 (La Película Interactiva):</b> Respondemos a la gran pregunta pendiente: "
        "<b>¿Es esa desigualdad una condena fija o se está cerrando la brecha con los fondos de cohesión?</b> "
        "Recorremos 25 años (2000–2024) con el reproductor temporal interactivo, demostrando empíricamente cómo la ratio "
        "P90/P10 se redujo de <b>4.2x a 2.4x</b> y analizando la ley de rendimientos decrecientes del PIB en el bienestar ciudadano.",
        style_speech
    )
    card_narrative = Table([[narrative_p]], colWidths=[499])
    card_narrative.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BLUE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(card_narrative)
    story.append(Spacer(1, 6))

    # 2. Tecnologías Empleadas y Alineación con Tema 3
    story.append(Paragraph("2. Stack Tecnológico y Alineación Exhaustiva con el Tema 3", style_sec_heading))
    
    tabla_tech = [
        [
            Paragraph("<b>Área / Módulo</b>", style_table_header),
            Paragraph("<b>Tecnología Usada</b>", style_table_header),
            Paragraph("<b>Concepto Clave del Tema 3 (Sesión 7 y 8)</b>", style_table_header),
            Paragraph("<b>Implementación Concreta en la App</b>", style_table_header)
        ],
        [
            Paragraph("<b>Web App & Reactividad</b>", style_table_header),
            Paragraph("<b>Plotly Dash</b> (Flask + React.js)", style_table_cell),
            Paragraph("<i>Streamlit vs Dash (Secc. 7):</i> Grafo de dependencias selectivas frente a la re-ejecución lineal total.", style_table_cell),
            Paragraph("Callbacks encadenados en <code>app.py</code> con actualización en cascada sin recargar la página.", style_table_cell)
        ],
        [
            Paragraph("<b>Inteligencia Geoespacial</b>", style_table_header),
            Paragraph("<b>Folium + Leaflet.js</b><br/><code>branca.colormap</code>", style_table_cell),
            Paragraph("<i>Folium y Leaflet (Secc. 5):</i> Mapas navegables embebidos con capas vectoriales y coropletas.", style_table_cell),
            Paragraph("Mapa coroplético en <code>iframe</code> (srcDoc) con GeoJSON, escala cromática continua y popups HTML.", style_table_cell)
        ],
        [
            Paragraph("<b>Gráficos Multivariantes</b>", style_table_header),
            Paragraph("<b>Plotly Express</b> &<br/><code>graph_objects</code>", style_table_cell),
            Paragraph("<i>Mantra de Shneiderman (1996) + Gapminder:</i> Overview first, zoom & filter, details on demand.", style_table_cell),
            Paragraph("Scatter logarítmico multidimensional (PIB vs longevidad) y serie temporal con <code>rangeslider</code>.", style_table_cell)
        ],
        [
            Paragraph("<b>Prevención de Errores</b>", style_table_header),
            Paragraph("Ejes estables y diseño decluttering", style_table_cell),
            Paragraph("<i>El Muro de los Horrores (Secc. 6):</i> Evitar saltos de escala en animación y muro de widgets.", style_table_cell),
            Paragraph("Ejes X/Y bloqueados en Scatter para evitar auto-escalado errático; KPIs independientes del hover.", style_table_cell)
        ],
        [
            Paragraph("<b>Motor Temporal</b>", style_table_header),
            Paragraph("<code>dcc.Interval</code> + Dash Buttons", style_table_cell),
            Paragraph("<i>Mecanismos de interactividad (Secc. 3):</i> Animación temporal continua controlada.", style_table_cell),
            Paragraph("Botón Play/Pausa que itera año a año a 1.2s actualizando mapa, ranking y tarjetas simultáneamente.", style_table_cell)
        ],
        [
            Paragraph("<b>Datos y Despliegue</b>", style_table_header),
            Paragraph("Pandas + GeoPandas<br/>Gunicorn + Docker", style_table_cell),
            Paragraph("<i>Del gráfico a la Web App (Secc. 7):</i> Servidores WSGI y despliegue cloud en producción.", style_table_cell),
            Paragraph("Dataset Banco Mundial (975 filas × 25 años) empaquetado en Docker y desplegado en Render.", style_table_cell)
        ]
    ]

    t_tech = Table(tabla_tech, colWidths=[80, 95, 164, 160])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 6))

    # 3. Cronograma Resumen
    story.append(Paragraph("3. Cronograma de Tiempos (5 Minutos)", style_sec_heading))
    tabla_tiempos = [
        [Paragraph("<b>Tiempo</b>", style_table_header), Paragraph("<b>Fase / Pestaña</b>", style_table_header), Paragraph("<b>Foco en Tecnologías del Tema 3 y Narrativa</b>", style_table_header)],
        [Paragraph("<b>00:00 – 00:45</b> (45s)", style_meta), Paragraph("Introducción general", style_meta), Paragraph("Enlace con Demo Day 1, formulación de la pregunta de negocio y arquitectura Dash.", style_meta)],
        [Paragraph("<b>00:45 – 02:15</b> (90s)", style_meta), Paragraph("Pestaña 1: Mapa Espacial", style_meta), Paragraph("<b>Folium + Leaflet, Branca, iframe y animación Play/Pausa (dcc.Interval)</b> a 1.2s/año.", style_meta)],
        [Paragraph("<b>02:15 – 03:30</b> (75s)", style_meta), Paragraph("Pestaña 2: Dinámica Plotly", style_meta), Paragraph("<b>Plotly Express (Gapminder)</b>, blindaje del <i>Muro de los Horrores</i> y series con <code>rangeslider</code>.", style_meta)],
        [Paragraph("<b>03:30 – 04:30</b> (60s)", style_meta), Paragraph("Arquitectura & Políticas", style_meta), Paragraph("<b>Mantra de Shneiderman</b>, reactividad en cascada, Docker/Render y fondos de cohesión.", style_meta)],
        [Paragraph("<b>04:30 – 05:00</b> (30s)", style_meta), Paragraph("Conclusiones & Q&A", style_meta), Paragraph("Síntesis de impacto social y apertura a preguntas del tribunal (1 min).", style_meta)],
    ]
    t_crono = Table(tabla_tiempos, colWidths=[90, 130, 279])
    t_crono.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_crono)

    # Forzar salto a página 2 para que el guion empiece limpio
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2 Y 3: GUION PASO A PASO CON ACCIONES Y DISCURSO LITERAL
    # =========================================================================
    story.append(Paragraph("4. Guion Literal y Acciones en Pantalla (Paso a Paso)", style_sec_heading))

    bloques = [
        {
            "num": "BLOQUE 1 | 00:00 – 00:45 (45 segundos)",
            "fase": "INTRODUCCIÓN: PUENTE CON DEMO DAY 1 Y ARQUITECTURA",
            "accion": "🖥️ PANTALLA: Dashboard abierto en http://localhost:8050. Pestaña 1 visible. Año 2000 en el slider.",
            "tech": "Conceptos Tema 3: Cambio de paradigma hacia exploración activa · Plotly Dash nativo (Flask WSGI) · Pregunta analítica.",
            "discurso": (
                "\"Buenos días. En el Demo Day 1 exploramos la distribución de la riqueza europea y demostramos lo que denominamos "
                "la <b>falacia de la media</b>: cómo unos pocos outliers financieros inflaban el PIB continental, dejando al 64% de las "
                "naciones por debajo del promedio y evidenciando una brecha de más de 30 a 1 entre extremos.<br/><br/>"
                "Sin embargo, aquello era una fotografía estática. Como vimos en el <b>Tema 3</b>, la verdadera toma de decisiones exige pasar "
                "de la narrativa cerrada a la <b>exploración activa</b>. La pregunta crítica que quedó abierta fue: <b>¿es esta desigualdad territorial "
                "un destino inmutable o se está cerrando la brecha con los fondos de cohesión?</b><br/><br/>"
                "Para responderlo, he desarrollado este <b>Observatorio de Cohesión Europea (2000–2024)</b>. Implementado de forma nativa en "
                "<b>Plotly Dash</b> sobre un servidor Flask/WSGI, el cuadro de mando permite explorar 25 años de microdatos del Banco Mundial "
                "con reactividad en tiempo real.\""
            )
        },
        {
            "num": "BLOQUE 2 | 00:45 – 02:15 (1 minuto y 30 segundos)",
            "fase": "PESTAÑA 1: DIAGNÓSTICO ESPACIAL (FOLIUM) Y MOTOR TEMPORAL (PLAY)",
            "accion": "👉 ACCIÓN: Señala los KPIs superiores. PULSA EL BOTÓN 'PLAY'. Deja correr la animación hasta 2024 (tarda ~25s) y pulsa 'Pausa'. Haz clic en un país (ej. Polonia o España).",
            "tech": "Conceptos Tema 3: Folium (Leaflet.js wrapper) · Capas GeoJSON · branca.colormap · Iframe dinámico · dcc.Interval (animación continua) · Details-on-Demand (popups HTML).",
            "discurso": (
                "\"En la barra superior monitorizamos los indicadores clave: PIB per cápita medio, longevidad y una métrica fundamental: "
                "la <b>ratio de brecha territorial (P90/P10)</b>, que compara el 10% más rico con el 10% más vulnerable.<br/><br/>"
                "<i>(Pulsas Play)</i> Fijaos en lo que ocurre al activar el reproductor temporal, gobernado por un componente <code>dcc.Interval</code> "
                "a 1.2 segundos por ejercicio. En el año 2000, la brecha de ingresos era de 4.2 veces. Pero a medida que la animación avanza —con "
                "las sucesivas ampliaciones de la UE— observamos en el mapa coroplético de <b>Folium</b> cómo Europa del Este (Polonia, Chequia, los Bálticos) "
                "pasa de tonos amarillos pálidos a tonos azules intensos.<br/><br/>"
                "<i>(Pausas en 2024)</i> En 2024, la brecha se ha reducido de <b>4.2x a 2.4x</b>. La convergencia ha sido real: naciones del Este han más que duplicado su renta.<br/><br/>"
                "<i>(Haces clic en Polonia o España)</i> Técnicamente, el mapa está encapsulado mediante un <code>iframe</code> dinámico que renderiza polígonos vectoriales GeoJSON "
                "con escalas continuas de <b>Branca</b>. Cumpliendo el mantra de Shneiderman de <i>Details-on-Demand</i>, al hacer clic en cualquier estado se abre un popup HTML con desglose "
                "estructural de PIB, salud e I+D, sincronizado con el ranking lateral.\""
            )
        },
        {
            "num": "BLOQUE 3 | 02:15 – 03:30 (1 minuto y 15 segundos)",
            "fase": "PESTAÑA 2: DINÁMICA TEMPORAL GAPMINDER (PLOTLY EXPRESS Y GRAPH_OBJECTS)",
            "accion": "👉 ACCIÓN: Cambia a la pestaña '📊 Dinámica Temporal & Gapminder'. Pasa el cursor por las burbujas. Mueve el RangeSlider inferior en la serie temporal de la derecha.",
            "tech": "Conceptos Tema 3: Plotly Express (px.scatter Gapminder) · plotly.graph_objects · RangeSlider / RangeSelector · Blindaje contra el Muro de los Horrores (límites estables sin saltos de escala).",
            "discurso": (
                "\"Pero la riqueza solo importa si genera bienestar ciudadano. Pasamos a la pestaña de dinámica temporal.<br/><br/>"
                "A la izquierda tenemos un gráfico multidimensional estilo <b>Gapminder</b> construido con <b>Plotly Express</b>: en el eje X el PIB per cápita en escala logarítmica, "
                "en el eje Y la esperanza de vida, tamaño codificado por población y colores por macrorregión.<br/><br/>"
                "Aquí descubrimos un principio económico esencial: la <b>ley de rendimientos decrecientes de la riqueza</b>. En tramos de desarrollo de $5.000 a $25.000, cada incremento "
                "de PIB dispara la longevidad de 68 a 78 años. Pero a partir de $40.000, la curva se aplana: el dinero por sí solo deja de comprar años de vida; la diferencia la marca la inversión en sanidad e innovación.<br/><br/>"
                "<i>(Señalas la serie temporal a la derecha)</i> Muy importante en términos del <b>Tema 3</b>: para esquivar la trampa del <b>Muro de los Horrores</b> (los saltos de escala "
                "automáticos en animaciones), hemos fijado límites rígidos en los ejes X e Y. Y en el gráfico de la derecha, implementado con <b>plotly.graph_objects</b>, contrastamos "
                "el país seleccionado con la media europea, permitiendo inspeccionar crisis con el <code>rangeslider</code>.\""
            )
        },
        {
            "num": "BLOQUE 4 | 03:30 – 04:30 (1 minuto exacto)",
            "fase": "ARQUITECTURA REACTIVA EN CASCADA Y SOPORTE A LA DECISIÓN",
            "accion": "👉 ACCIÓN: Cambia el desplegable de Macrorregión a 'Europa del Sur'. Muestra cómo el selector de país se filtra al instante. Menciona el despliegue en Render.",
            "tech": "Conceptos Tema 3: Grafo de reactividad en Dash (@app.callback encadenados) · Filtros en cascada · Herramienta de soporte a la decisión · Despliegue en producción Docker/Render.",
            "discurso": (
                "\"La interactividad de este cuadro de mando responde al <b>Mantra de Shneiderman</b>: <i>Overview first, zoom and filter, then details-on-demand</i>.<br/><br/>"
                "Fijaos en la reactividad: si selecciono 'Europa del Sur', un <b>callback encadenado</b> actualiza en cascada el desplegable de países para mostrar solo los estados de dicha región, "
                "recalculando al mismo tiempo los KPIs superiores sin recargar el DOM. Esto demuestra la superioridad de la arquitectura de <b>Dash frente a scripts lineales</b>.<br/><br/>"
                "¿Qué decisión apoya esta herramienta? Evidencia a los comités de cohesión de la UE que las transferencias financieras tradicionales ya no bastan: para escapar de la trampa del ingreso medio, "
                "las ayudas deben condicionarse a elevar el gasto en I+D tecnológica por encima del 2.5% del PIB y acelerar la transición renovable.<br/><br/>"
                "En cuanto a producción: la app se ejecuta en local con <code>python lab_sol.py</code> y está plenamente operativa en la nube en <b>Render</b> mediante un contenedor Docker con SSL.\""
            )
        },
        {
            "num": "BLOQUE 5 | 04:30 – 05:00 (30 segundos)",
            "fase": "CONCLUSIÓN EJECUTIVA Y TURNO DE PREGUNTAS (1 MIN)",
            "accion": "🖥️ PANTALLA: Vuelve a la pestaña 1 con el mapa de 2024 visible. Mira de frente al profesor.",
            "tech": "Conceptos Tema 3: Storytelling efectivo · Soporte a la decisión pública · Cierre riguroso.",
            "discurso": (
                "\"En conclusión: en el Demo Day 1 presentamos una foto estática de fractura y asimetría estadística. Hoy hemos demostrado que "
                "Europa ha vivido una convergencia real, reduciendo su brecha territorial casi a la mitad.<br/><br/>"
                "Como aprendimos en el <b>Tema 3</b>, la visualización interactiva no consiste en acumular widgets, sino en estructurar un flujo analítico "
                "que transforme datos complejos en soporte a la decisión pública.<br/><br/>"
                "Muchas gracias por su atención; el proyecto está disponible en local y en Render, y quedo a su disposición para cualquier pregunta.\""
            )
        }
    ]

    for i, b in enumerate(bloques):
        # Insertar saltos de página para tener 2 bloques por página y el bloque final en la página 4
        if i == 2 or i == 4:
            story.append(PageBreak())

        card_content = [
            [Paragraph(f"<b>{b['num']}</b> — <font color='#2563EB'>{b['fase']}</font>", style_badge)],
            [Paragraph(f"<b>{b['accion']}</b>", style_action)],
            [Paragraph(f"<b>🔗 ALINEACIÓN TEMA 3:</b> <font color='#475569'>{b['tech']}</font>", style_meta)],
            [Paragraph(b['discurso'], style_speech)]
        ]
        t_b = Table(card_content, colWidths=[499])
        t_b.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,0), 0.5, C_BORDER),
            ('LINEBELOW', (0,1), (-1,1), 0.5, C_BORDER),
            ('LINEBELOW', (0,2), (-1,2), 0.5, C_BORDER),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F8FAFC")),
            ('BACKGROUND', (0,1), (-1,1), C_AMBER_LIGHT),
            ('BACKGROUND', (0,2), (-1,2), C_PURPLE_LIGHT),
        ]))
        story.append(t_b)
        story.append(Spacer(1, 6))

    # =========================================================================
    # MATRIZ TEÓRICA DEL TEMA 3 Y CLAVES DE ORATORIA (PÁGINA 4)
    # =========================================================================
    story.append(Paragraph("5. Matriz Teórica del Tema 3 Evaluada en la Rúbrica", style_sec_heading))
    
    matriz_tema3 = [
        [
            Paragraph("<b>Concepto Teórico (Tema 3)</b>", style_table_header),
            Paragraph("<b>Trampa Teórica o Desafío</b>", style_table_header),
            Paragraph("<b>Solución y Blindaje Implementado en el Código</b>", style_table_header)
        ],
        [
            Paragraph("<b>Mantra de Shneiderman</b><br/>(1996)", style_table_header),
            Paragraph("Presentar visualizaciones saturadas o colecciones caóticas de datos.", style_table_cell),
            Paragraph("Flujo en 3 pasos: 1. Overview continental (mapa/KPIs) → 2. Zoom & Filter (Play timeline, filtros región) → 3. Details-on-Demand (popups HTML Folium y hover Plotly).", style_table_cell)
        ],
        [
            Paragraph("<b>El Muro de los Horrores:</b><br/>Saltos de Escala (Trampa III)", style_table_header),
            Paragraph("Auto-escalado dinámico que reajusta ejes X/Y en cada fotograma mareando al usuario.", style_table_cell),
            Paragraph("En <code>fig_scatter</code> se fijaron rangos rígidos <code>range=[2.5, 5.3]</code> y <code>range=[65, 87]</code> para asegurar una animación suave sin saltos.", style_table_cell)
        ],
        [
            Paragraph("<b>El Muro de los Horrores:</b><br/>Sobrecarga de Widgets (Trampa I)", style_table_header),
            Paragraph("Muro de controles aislados sin relación analítica coherente.", style_table_cell),
            Paragraph("Filtros globales agrupados en una sola tarjeta con selectores en cascada (Región → filtra Países automáticamente) evitando estados inconsistentes.", style_table_cell)
        ],
        [
            Paragraph("<b>El Muro de los Horrores:</b><br/>Dependencia del Hover (Trampa V)", style_table_header),
            Paragraph("Ocultar las conclusiones críticas detrás del movimiento forzado del ratón.", style_table_cell),
            Paragraph("Tarjetas de KPIs superiores (PIB medio, ratio P90/P10) y ranking lateral Top 5 / Bottom 5 visibles en todo momento sin requerir hover.", style_table_cell)
        ],
        [
            Paragraph("<b>Arquitectura Web App:</b><br/>Dash vs. Streamlit (Secc. 7)", style_table_header),
            Paragraph("Re-ejecución total del script lineal ante cualquier interacción (Streamlit).", style_table_cell),
            Paragraph("Plotly Dash ejecuta un grafo de dependencias reactivas selectivas (<code>@app.callback</code>), actualizando solo el elemento afectado a 1.2s/año.", style_table_cell)
        ]
    ]

    t_matriz = Table(matriz_tema3, colWidths=[110, 155, 234])
    t_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_matriz)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Claves de Oratoria y Defensa Oral", style_sec_heading))
    tips_text = (
        "<b>1. Deja trabajar al motor de animación:</b> Al pulsar 'Play', habla pausado durante los 25s de recorrido. El mapa de Folium captará la atención del tribunal de forma natural.<br/>"
        "<b>2. Cita expresamente el 'Mantra de Shneiderman' y el 'Muro de los Horrores':</b> Demuestra al profesor Jorge Dueñas que has interiorizado los principios metodológicos de las transparencias.<br/>"
        "<b>3. Destaca la arquitectura Dash frente a Streamlit:</b> Subraya que la reactividad se basa en callbacks encadenados selectivos sin re-ejecución total del script.<br/>"
        "<b>4. Cierre con 'lab_sol.py' y Render:</b> Recordar que está en local y desplegado en producción garantiza la puntuación máxima de reproducibilidad y rigor técnico."
    )
    card_tips = Table([[Paragraph(tips_text, style_tip)]], colWidths=[499])
    card_tips.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_GREEN_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(card_tips)

    # Compilar documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito en: {pdf_path}")

if __name__ == '__main__':
    generar_pdf()
