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
    AltoDeLinea=5, 
    EspacioEntreLineas=4,
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
        
        if col < columnas - 1:
            x_linea_divisoria = x_start + ancho_columna + (margenEntreColumnas * mm / 2)
            c.line(x_linea_divisoria, y_start, x_linea_divisoria, y_start + alto_util)
        
        y_actual = alto_pagina - (margenVertical * mm)
        while True:
            y_actual -= (AltoDeLinea * mm)
            if y_actual <= y_start:
                break
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)
            y_actual -= (EspacioEntreLineas * mm)
            if y_actual <= y_start:
                break
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)

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
            draw.line(
                [(x_start_px, y_actual_px), (x_start_px + ancho_columna_px, y_actual_px)], 
                fill=color, 
                width=line_width
            )
            
            y_actual_px += (EspacioEntreLineas * ppm)
            if y_actual_px >= y_start_px + alto_util_px:
                break
            draw.line(
                [(x_start_px, y_actual_px), (x_start_px + ancho_columna_px, y_actual_px)], 
                fill=color, 
                width=line_width
            )

    # Guardar con metadatos de DPI para que al imprimir respete el tamaño físico
    img.save(output_jpg_path, 'JPEG', quality=95, dpi=(dpi, dpi))

# Ejemplo de uso
if __name__ == "__main__":
    generar_documentos_columnas()