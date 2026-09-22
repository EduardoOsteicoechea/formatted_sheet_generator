from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from PIL import Image, ImageDraw, ImageColor

def generar_documentos_columnas(
    margenLateral=20, 
    margenVertical=10, 
    margenEntreColumnas=20, 
    columnas=3, 
    grosorDeBorde=0.25, 
    colorDeGrosorDeBorde='#eeeeee', 
    AltoDeLinea=4, 
    EspacioEntreLineas=3,
    output_pdf_path='documento_generado_columnas.pdf',
    output_jpg_path='documento_generado_columnas.jpg'
):
    """
    Genera un PDF vectorial y un JPG de alta resolución (300 DPI) 
    tamaño US Letter (Vertical) con las mismas especificaciones.
    """
    
    # ---------------------------------------------------------
    # 1. GENERACIÓN DEL PDF (REPORTLAB)
    # ---------------------------------------------------------
    ancho_pagina, alto_pagina = letter
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setLineWidth(grosorDeBorde * mm)
    c.setStrokeColor(HexColor(colorDeGrosorDeBorde))
    
    ancho_util = ancho_pagina - (2 * margenLateral * mm)
    alto_util = alto_pagina - (2 * margenVertical * mm)
    ancho_columna = (ancho_util - (columnas - 1) * margenEntreColumnas * mm) / columnas
    
    for col in range(columnas):
        x_start = (margenLateral * mm) + col * (ancho_columna + margenEntreColumnas * mm)
        y_start = margenVertical * mm
        
        c.rect(x_start, y_start, ancho_columna, alto_util)
        # Línea superior del primer renglón (mismo tono oscuro que la inferior)
        c.setStrokeColor(HexColor('#dddddd'))
        c.line(x_start, y_start + alto_util, x_start + ancho_columna, y_start + alto_util)
        c.setStrokeColor(HexColor(colorDeGrosorDeBorde))
        
        if col < columnas - 1:
            x_linea_divisoria = x_start + ancho_columna + (margenEntreColumnas * mm / 2)
            c.line(x_linea_divisoria, y_start, x_linea_divisoria, y_start + alto_util)
        
        y_actual = alto_pagina - (margenVertical * mm)
        while True:
            y_actual -= (AltoDeLinea * mm)
            if y_actual <= y_start:
                break
            # Línea inferior del renglón de AltoDeLinea (un poco más oscura)
            c.setStrokeColor(HexColor('#dddddd'))
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)
            c.setStrokeColor(HexColor(colorDeGrosorDeBorde))
            # Renglón de 4 mm: bandas 1.1 | 1.8 | 1.1 mm (no tercios iguales)
            seccion_extrema = 1.1
            c.line(
                x_start, y_actual + (AltoDeLinea - seccion_extrema) * mm,
                x_start + ancho_columna, y_actual + (AltoDeLinea - seccion_extrema) * mm
            )
            c.line(
                x_start, y_actual + seccion_extrema * mm,
                x_start + ancho_columna, y_actual + seccion_extrema * mm
            )
            y_actual -= (EspacioEntreLineas * mm)
            if y_actual <= y_start:
                break
            # Línea superior del siguiente renglón (cierre del espacio de 3 mm, un poco más oscura)
            c.setStrokeColor(HexColor('#dddddd'))
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)
            c.setStrokeColor(HexColor(colorDeGrosorDeBorde))
            # Espacio de 3 mm dividido en 3 partes de 1 mm
            seccion_espacio = EspacioEntreLineas / 3
            c.line(
                x_start, y_actual + (EspacioEntreLineas - seccion_espacio) * mm,
                x_start + ancho_columna, y_actual + (EspacioEntreLineas - seccion_espacio) * mm
            )
            c.line(
                x_start, y_actual + seccion_espacio * mm,
                x_start + ancho_columna, y_actual + seccion_espacio * mm
            )

    c.save()

    # ---------------------------------------------------------
    # 2. GENERACIÓN DEL JPG (PILLOW)
    # ---------------------------------------------------------
    dpi = 300
    ppm = dpi / 25.4  # Píxeles por milímetro exactos
    
    # Tamaño US Letter exacto en píxeles a 300 DPI (8.5 x 11 pulgadas = 2550 x 3300 píxeles)
    ancho_px = int(8.5 * dpi)
    alto_px = int(11.0 * dpi)
    
    # Crear un lienzo blanco
    img = Image.new('RGB', (ancho_px, alto_px), 'white')
    draw = ImageDraw.Draw(img)
    
    color = ImageColor.getrgb(colorDeGrosorDeBorde)
    line_width = max(1, int(grosorDeBorde * ppm))
    
    ml_px = margenLateral * ppm
    mv_px = margenVertical * ppm
    mc_px = margenEntreColumnas * ppm
    
    ancho_util_px = ancho_px - (2 * ml_px)
    alto_util_px = alto_px - (2 * mv_px)
    ancho_columna_px = (ancho_util_px - (columnas - 1) * mc_px) / columnas
    
    for col in range(columnas):
        # A diferencia de ReportLab, PIL tiene su coordenada Y=0 en la parte SUPERIOR
        x_start_px = ml_px + col * (ancho_columna_px + mc_px)
        y_start_px = mv_px 
        
        # Rectángulo de la columna
        draw.rectangle(
            [x_start_px, y_start_px, x_start_px + ancho_columna_px, y_start_px + alto_util_px], 
            outline=color, 
            width=line_width
        )
        # Línea superior del primer renglón (mismo tono oscuro que la inferior)
        color_oscuro = ImageColor.getrgb('#dddddd')
        draw.line(
            [(x_start_px, y_start_px), (x_start_px + ancho_columna_px, y_start_px)],
            fill=color_oscuro,
            width=line_width
        )
        
        # Línea divisoria vertical
        if col < columnas - 1:
            x_linea_px = x_start_px + ancho_columna_px + (mc_px / 2)
            draw.line(
                [(x_linea_px, y_start_px), (x_linea_px, y_start_px + alto_util_px)], 
                fill=color, 
                width=line_width
            )
            
        # Renglones internos (dibujando de arriba hacia abajo)
        y_actual_px = y_start_px
        while True:
            y_actual_px += (AltoDeLinea * ppm)
            if y_actual_px >= y_start_px + alto_util_px:
                break
            # Línea inferior del renglón de AltoDeLinea (un poco más oscura)
            draw.line(
                [(x_start_px, y_actual_px), (x_start_px + ancho_columna_px, y_actual_px)], 
                fill=color_oscuro, 
                width=line_width
            )
            # Renglón de 4 mm: bandas 1.1 | 1.8 | 1.1 mm (no tercios iguales)
            seccion_extrema = 1.1
            y_interna_sup = y_actual_px - (AltoDeLinea - seccion_extrema) * ppm
            y_interna_inf = y_actual_px - seccion_extrema * ppm
            draw.line(
                [(x_start_px, y_interna_sup), (x_start_px + ancho_columna_px, y_interna_sup)],
                fill=color,
                width=line_width
            )
            draw.line(
                [(x_start_px, y_interna_inf), (x_start_px + ancho_columna_px, y_interna_inf)],
                fill=color,
                width=line_width
            )
            
            y_actual_px += (EspacioEntreLineas * ppm)
            if y_actual_px >= y_start_px + alto_util_px:
                break
            # Línea superior del siguiente renglón (cierre del espacio de 3 mm, un poco más oscura)
            draw.line(
                [(x_start_px, y_actual_px), (x_start_px + ancho_columna_px, y_actual_px)], 
                fill=color_oscuro, 
                width=line_width
            )
            # Espacio de 3 mm dividido en 3 partes de 1 mm
            seccion_espacio = EspacioEntreLineas / 3
            y_esp_sup = y_actual_px - (EspacioEntreLineas - seccion_espacio) * ppm
            y_esp_inf = y_actual_px - seccion_espacio * ppm
            draw.line(
                [(x_start_px, y_esp_sup), (x_start_px + ancho_columna_px, y_esp_sup)],
                fill=color,
                width=line_width
            )
            draw.line(
                [(x_start_px, y_esp_inf), (x_start_px + ancho_columna_px, y_esp_inf)],
                fill=color,
                width=line_width
            )

    # Guardar con metadatos de DPI para que al imprimir respete el tamaño físico
    img.save(output_jpg_path, 'JPEG', quality=95, dpi=(dpi, dpi))

# Ejemplo de uso
if __name__ == "__main__":
    generar_documentos_columnas(
        output_pdf_path='documento_generado_columnas_v2.pdf',
        output_jpg_path='documento_generado_columnas_v2.jpg'
    )