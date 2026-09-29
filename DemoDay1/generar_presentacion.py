import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def crear_presentacion():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]  # Diapositiva en blanco

    # Paleta de colores ejecutiva
    C_BG = RGBColor(250, 250, 250)         # #FAFAFA
    C_NAVY = RGBColor(15, 23, 42)          # #0F172A (Texto principal / títulos)
    C_BLUE = RGBColor(2, 132, 199)         # #0284C7 (Acento corporativo)
    C_BLUE_DARK = RGBColor(0, 98, 155)     # #00629B
    C_RED = RGBColor(217, 33, 33)          # #D92121 (Acento de alerta)
    C_MUTED = RGBColor(100, 116, 139)      # #64748B (Texto secundario)
    C_CARD_BG = RGBColor(255, 255, 255)    # Blanco puro para tarjetas
    C_CARD_BORDER = RGBColor(226, 232, 240)# #E2E8F0
    C_HIGHLIGHT_BG = RGBColor(241, 245, 249) # #F1F5F9

    def agregar_fondo(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def agregar_cabecera(slide, categoria, titulo, subtitulo=""):
        # Categoría / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = categoria.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE

        # Título principal
        tit_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.55))
        tf_tit = tit_box.text_frame
        tf_tit.word_wrap = True
        tf_tit.margin_left = tf_tit.margin_top = tf_tit.margin_right = tf_tit.margin_bottom = 0
        p_tit = tf_tit.paragraphs[0]
        p_tit.text = titulo
        p_tit.font.size = Pt(20)
        p_tit.font.bold = True
        p_tit.font.color.rgb = C_NAVY

        if subtitulo:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitulo
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s1)

    # Acento superior sutil
    barra = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(1.2), Inches(0.08))
    barra.fill.solid()
    barra.fill.fore_color.rgb = C_BLUE
    barra.line.fill.background()

    # Título Portada
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.9), Inches(11.5), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "La Brecha de Prosperidad Europea"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Asimetrías Territoriales y Distribución de Riqueza en 39 Naciones"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_BLUE_DARK
    p2.space_after = Pt(16)

    p3 = tf1.add_paragraph()
    p3.text = "Un análisis empírico sobre la desconexión entre masa económica agregada y bienestar ciudadano real."
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_MUTED

    # Tarjeta de metadatos académicos / autor
    meta_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.733), Inches(1.8))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = C_CARD_BG
    meta_card.line.color.rgb = C_CARD_BORDER
    meta_card.line.width = Pt(1)

    m_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.1), Inches(11.0), Inches(1.2))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True

    pm1 = tf_m.paragraphs[0]
    pm1.text = "DEMO DAY 1  |  SPRINT 1: EL ARTE DE LOS DATOS ESTÁTICOS"
    pm1.font.size = Pt(10.5)
    pm1.font.bold = True
    pm1.font.color.rgb = C_BLUE
    pm1.space_after = Pt(6)

    pm2 = tf_m.add_paragraph()
    pm2.text = "Autor: Javier  •  Asignatura: Visualización y Análisis de Datos (VAD)  •  Universidad Politécnica de Madrid (UPM)"
    pm2.font.size = Pt(12)
    pm2.font.bold = True
    pm2.font.color.rgb = C_NAVY
    pm2.space_after = Pt(4)

    pm3 = tf_m.add_paragraph()
    pm3.text = "Dataset: europe.geojson (39 países)  •  Stack: Python, GeoPandas, Matplotlib & Seaborn (Clean Script)"
    pm3.font.size = Pt(11)
    pm3.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 2: MOTIVACIÓN Y ENFOQUE ANALÍTICO
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s2)
    agregar_cabecera(s2, "Contexto Situacional", "El Reto de la Cohesión Territorial en Europa", 
                     "Por qué los indicadores agregados enmascaran la realidad económica del continente")

    tarjetas_s2 = [
        ("1. La Pregunta Central", 
         "¿Refleja el PIB nacional bruto la calidad de vida de los ciudadanos?", 
         "Las métricas agregadas sitúan a Europa como una de las regiones más ricas del planeta, pero ocultan una dispersión extrema en la capacidad adquisitiva real por habitante."),
        
        ("2. Objetivos de Investigación", 
         "Cuantificar la fractura este-oeste y el desacoplamiento de escala", 
         "• Contrastar si el tamaño demográfico/económico garantiza bienestar individual.\n• Evaluar la validez de la media aritmética como baremo para fondos de cohesión."),
        
        ("3. Criterio Metodológico", 
         "Visualización explicativa rigurosa y libre de ruido (Decluttering)", 
         "• Eliminación total de bordes y leyendas complejas mediante anotaciones directas.\n• Foco preatencional estricto: contraste cromático directo sobre las anomalías.")
    ]

    left_pos = 0.8
    for t_cat, t_tit, t_desc in tarjetas_s2:
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(2.0), Inches(3.64), Inches(4.7))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1)

        c_box = s2.shapes.add_textbox(Inches(left_pos + 0.25), Inches(2.3), Inches(3.14), Inches(4.1))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True

        p_c1 = tf_c.paragraphs[0]
        p_c1.text = t_cat.upper()
        p_c1.font.size = Pt(9.5)
        p_c1.font.bold = True
        p_c1.font.color.rgb = C_BLUE
        p_c1.space_after = Pt(10)

        p_c2 = tf_c.add_paragraph()
        p_c2.text = t_tit
        p_c2.font.size = Pt(13)
        p_c2.font.bold = True
        p_c2.font.color.rgb = C_NAVY
        p_c2.space_after = Pt(12)

        p_c3 = tf_c.add_paragraph()
        p_c3.text = t_desc
        p_c3.font.size = Pt(11)
        p_c3.font.color.rgb = C_MUTED

        left_pos += 4.04

    # =========================================================================
    # DIAPOSITIVA 3: GRÁFICO 1 - MAPA DE DISTRIBUCIÓN
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s3)
    agregar_cabecera(s3, "Dimensión Espacial", "La Fractura Territorial de Europa: Eje Central vs. Periferia",
                     "Mapa coroplético del PIB per cápita con anotaciones directas y mitigación de sesgos")

    # Imagen a la izquierda
    img_mapa = "figuras/grafico_1_mapa_europa.png"
    if os.path.exists(img_mapa):
        s3.shapes.add_picture(img_mapa, Inches(0.8), Inches(1.85), width=Inches(7.6))

    # Panel analítico a la derecha
    p_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.85), Inches(3.83), Inches(5.0))
    p_card.fill.solid()
    p_card.fill.fore_color.rgb = C_CARD_BG
    p_card.line.color.rgb = C_CARD_BORDER
    p_card.line.width = Pt(1)

    pb = s3.shapes.add_textbox(Inches(9.0), Inches(2.1), Inches(3.23), Inches(4.5))
    tf_pb = pb.text_frame
    tf_pb.word_wrap = True

    p = tf_pb.paragraphs[0]
    p.text = "HALLAZGOS CLAVE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(8)

    p = tf_pb.add_paragraph()
    p.text = "• Concentración de Prosperidad:\nEl bloque central y nórdico (Suiza, Luxemburgo, Noruega, Dinamarca) supera con holgura los $60.000 de renta anual por habitante."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf_pb.add_paragraph()
    p.text = "• Franja de Vulnerabilidad:\nLos Balcanes y Ucrania registran rentas inferiores a los $10.000 anuales, conformando una periferia estructuralmente descolgada."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tf_pb.add_paragraph()
    p.text = "DECISIONES DE DISEÑO"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(4)

    p = tf_pb.add_paragraph()
    p.text = "• Rusia en gris neutro: Se neutraliza para evitar que su inmensa masa territorial distorsione la percepción cromática del continente.\n• Anotaciones directas in-situ para suprimir leyendas flotantes."
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 4: GRÁFICO 2 - POLARIZACIÓN EXTREMA (TOP 5 VS BOTTOM 5)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s4)
    agregar_cabecera(s4, "Magnitud de la Brecha", "Polarización Crítica: Top 5 frente al Bottom 5 Continental",
                     "Contraste del PIB per cápita con barras horizontales y rotulado directo de valores")

    img_barras = "figuras/grafico_2_brecha_extremos.png"
    if os.path.exists(img_barras):
        s4.shapes.add_picture(img_barras, Inches(0.8), Inches(1.85), width=Inches(7.6))

    p_card2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.85), Inches(3.83), Inches(5.0))
    p_card2.fill.solid()
    p_card2.fill.fore_color.rgb = C_CARD_BG
    p_card2.line.color.rgb = C_CARD_BORDER
    p_card2.line.width = Pt(1)

    pb2 = s4.shapes.add_textbox(Inches(9.0), Inches(2.1), Inches(3.23), Inches(4.5))
    tf_pb2 = pb2.text_frame
    tf_pb2.word_wrap = True

    p = tf_pb2.paragraphs[0]
    p.text = "DISPARIDAD DE 33 A 1"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(8)

    p = tf_pb2.add_paragraph()
    p.text = "• El Abismo de Ingresos:\nUn habitante en Luxemburgo (~$114k) genera 33 veces más renta anual que un habitante en Ucrania (~$3.5k)."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf_pb2.add_paragraph()
    p.text = "• Homogeneidad en el Rezagamiento:\nEl Bottom 5 completo (Ucrania, Moldavia, Kosovo, Albania, Macedonia) no supera los $6.5k anuales por persona."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tf_pb2.add_paragraph()
    p.text = "DECISIONES DE DISEÑO"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(4)

    p = tf_pb2.add_paragraph()
    p.text = "• Barras horizontales: Eliminan el cuello torcido y permiten leer los nombres sin inclinación.\n• Foco preatencional: Colores intensos en el líder y el rezagado; tonos pastel para el resto."
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 5: GRÁFICO 3 - VOLUMEN BRUTO VS PRODUCTIVIDAD INDIVIDUAL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s5)
    agregar_cabecera(s5, "Estructura Macroeconómica", "Volumen Nacional vs. Bienestar Individual: La Disociación",
                     "Relación bivariada entre tamaño demográfico, masa productiva total y PIB per cápita")

    img_scatter = "figuras/grafico_3_dispersion_pib_poblacion.png"
    if os.path.exists(img_scatter):
        s5.shapes.add_picture(img_scatter, Inches(0.8), Inches(1.85), width=Inches(7.6))

    p_card3 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.85), Inches(3.83), Inches(5.0))
    p_card3.fill.solid()
    p_card3.fill.fore_color.rgb = C_CARD_BG
    p_card3.line.color.rgb = C_CARD_BORDER
    p_card3.line.width = Pt(1)

    pb3 = s5.shapes.add_textbox(Inches(9.0), Inches(2.1), Inches(3.23), Inches(4.5))
    tf_pb3 = pb3.text_frame
    tf_pb3.word_wrap = True

    p = tf_pb3.paragraphs[0]
    p.text = "DESACOPLAMIENTO DE ESCALA"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(8)

    p = tf_pb3.add_paragraph()
    p.text = "• Potencias Industriales:\nAlemania, Reino Unido, Francia e Italia acumulan la mayor masa económica total, pero presentan rentas intermedias ($40k-$50k)."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf_pb3.add_paragraph()
    p.text = "• Especialización Eficiente:\nLos países con mayor renta por persona (Suiza, Luxemburgo, Noruega) no son gigantes demográficos, sino economías hiper-especializadas."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tf_pb3.add_paragraph()
    p.text = "DECISIONES DE DISEÑO"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(4)

    p = tf_pb3.add_paragraph()
    p.text = "• Anotaciones directas con flechas: Rotulación limpia sólo sobre las naciones estratégicas.\n• Barra continua lateral de color sin contorno exterior (Tufte)."
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 6: GRÁFICO 4 - ASIMETRÍA Y FALACIA DE LA MEDIA
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s6)
    agregar_cabecera(s6, "Diagnóstico Estadístico", "La Falacia de la Media: Distribución Sesgada del Bienestar",
                     "Histograma y estimación de densidad KDE demostrando el sesgo positivo del PIB per cápita")

    img_dist = "figuras/grafico_4_distribucion_sesgo.png"
    if os.path.exists(img_dist):
        s6.shapes.add_picture(img_dist, Inches(0.8), Inches(1.85), width=Inches(7.6))

    p_card4 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.85), Inches(3.83), Inches(5.0))
    p_card4.fill.solid()
    p_card4.fill.fore_color.rgb = C_CARD_BG
    p_card4.line.color.rgb = C_CARD_BORDER
    p_card4.line.width = Pt(1)

    pb4 = s6.shapes.add_textbox(Inches(9.0), Inches(2.1), Inches(3.23), Inches(4.5))
    tf_pb4 = pb4.text_frame
    tf_pb4.word_wrap = True

    p = tf_pb4.paragraphs[0]
    p.text = "EL 64% BAJO LA MEDIA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(8)

    p = tf_pb4.add_paragraph()
    p.text = "• Sesgo Positivo Pronunciado:\nLa media continental ($36.9k) está artificialmente inflada por outliers financieros extremos (Luxemburgo, Suiza)."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    p = tf_pb4.add_paragraph()
    p.text = "• La Mediana como Realidad:\nEl país representativo europeo se sitúa en $24.7k. Casi dos tercios (64%) de las naciones quedan por debajo del promedio oficial."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tf_pb4.add_paragraph()
    p.text = "DECISIONES DE DISEÑO"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(4)

    p = tf_pb4.add_paragraph()
    p.text = "• Líneas de corte explícitas: Diferenciación semántica inmediata entre media (azul continua) y mediana (roja discontinua) sin leyendas."
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # =========================================================================
    # DIAPOSITIVA 7: CONCLUSIONES Y RECOMENDACIONES ESTRATÉGICAS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s7)
    agregar_cabecera(s7, "Síntesis Ejecutiva", "Conclusiones y Recomendaciones de Política Pública",
                     "Propuestas concretas para la reasignación eficiente de fondos de cohesión comunitaria")

    # Columna izquierda: 3 Conclusiones analíticas
    card_c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.65), Inches(4.7))
    card_c.fill.solid()
    card_c.fill.fore_color.rgb = C_CARD_BG
    card_c.line.color.rgb = C_CARD_BORDER
    card_c.line.width = Pt(1)

    tfc = s7.shapes.add_textbox(Inches(1.1), Inches(2.25), Inches(5.05), Inches(4.2)).text_frame
    tfc.word_wrap = True

    p = tfc.paragraphs[0]
    p.text = "TRES CONCLUSIONES EMPÍRICAS"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)

    p = tfc.add_paragraph()
    p.text = "1. Disparidad Crítica (33x):\nEuropa no es un bloque homogéneo; coexisten estándares de máxima prosperidad global con bolsas de precariedad en el sureste continental."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tfc.add_paragraph()
    p.text = "2. Desconexión Volumen / Bienestar:\nEl tamaño económico nacional bruto no garantiza riqueza ciudadana. Las naciones intermedias especializadas ofrecen mayores rentas."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(12)

    p = tfc.add_paragraph()
    p.text = "3. Inadecuación de la Media:\nCon un 64% de países bajo el promedio, basar los diagnósticos en la media induce a decisiones presupuestarias distorsionadas."
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY

    # Columna derecha: 2 Recomendaciones estratégicas
    card_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(2.0), Inches(5.65), Inches(4.7))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_CARD_BG
    card_r.line.color.rgb = C_CARD_BORDER
    card_r.line.width = Pt(1)

    tfr = s7.shapes.add_textbox(Inches(7.15), Inches(2.25), Inches(5.05), Inches(4.2)).text_frame
    tfr.word_wrap = True

    p = tfr.paragraphs[0]
    p.text = "LLAMADA A LA ACCIÓN (POLÍTICAS PÚBLICAS)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(12)

    p = tfr.add_paragraph()
    p.text = "• Baremo basado en la Mediana Continental:\nReestructurar los criterios de asignación de los Fondos Estructurales utilizando la distancia a la mediana ($24.7k), protegiendo la asignación a las naciones de renta real media-baja."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(18)

    p = tfr.add_paragraph()
    p.text = "• Inversión Focalizada en el Eje Balcánico:\nPriorizar ayudas comunitarias en modernización industrial, conectividad e infraestructuras digitales en la franja oriental para frenar la fuga de talento y la polarización regional."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # DIAPOSITIVA 8: FICHA TÉCNICA Y DECLARACIÓN DE IA
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    agregar_fondo(s8)
    agregar_cabecera(s8, "Rigor Técnico y Metodológico", "Pipeline de Visualización y Transparencia de Herramientas",
                     "Cumplimiento explícito de los requisitos de reproducibilidad y rúbricas del Demo Day 1")

    t_s8 = [
        ("Pipeline Técnico", 
         "Script Reproducible lab_sol.py", 
         "• Programación estructurada y modular con ejecución integral directa.\n• Exportación dual: .pdf vectorial sin pérdida y .png a 300 DPI.\n• API orientada a objetos (fig, ax = plt.subplots).\n• Control fino de paletas sin leyendas redundantes."),
        
        ("Principios de Diseño", 
         "Edward Tufte & Gestalt", 
         "• Decluttering estricto: sns.despine() en todas las gráficas.\n• Eliminación del efecto cuello torcido mediante barras horizontales.\n• Maximización del Data-Ink Ratio.\n• Atributos preatencionales: Color selectivo sobre anomalías."),
        
        ("Declaración de IA", 
         "Uso Transparente de Herramientas", 
         "• Herramienta: Antigravity (Google DeepMind).\n• Alcance: Asistencia en la optimización de código, estructuración analítica de la narrativa y verificación de estándares visuales de la rúbrica oficial.")
    ]

    left_pos = 0.8
    for t_cat, t_tit, t_desc in t_s8:
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(2.0), Inches(3.64), Inches(4.7))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1)

        c_box = s8.shapes.add_textbox(Inches(left_pos + 0.25), Inches(2.3), Inches(3.14), Inches(4.1))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True

        p_c1 = tf_c.paragraphs[0]
        p_c1.text = t_cat.upper()
        p_c1.font.size = Pt(9.5)
        p_c1.font.bold = True
        p_c1.font.color.rgb = C_BLUE
        p_c1.space_after = Pt(10)

        p_c2 = tf_c.add_paragraph()
        p_c2.text = t_tit
        p_c2.font.size = Pt(13)
        p_c2.font.bold = True
        p_c2.font.color.rgb = C_NAVY
        p_c2.space_after = Pt(12)

        p_c3 = tf_c.add_paragraph()
        p_c3.text = t_desc
        p_c3.font.size = Pt(11)
        p_c3.font.color.rgb = C_MUTED

        left_pos += 4.04

    # Guardar presentación
    nombre_archivo = "presentacion_demo_day_1.pptx"
    prs.save(nombre_archivo)
    print(f"Presentación creada con éxito: {nombre_archivo}")

if __name__ == "__main__":
    crear_presentacion()
