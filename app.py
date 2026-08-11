from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

def generar_pdf_columnas(
    margenLateral=20, 
    margenVertical=10, 
    margenEntreColumnas=20, 
    columnas=3, 
    grosorDeBorde=0.25, 
    colorDeGrosorDeBorde='#eeeeee', 
    AltoDeLinea=5, 
    EspacioEntreLineas=4,
    output_path='documento_generado.pdf'
):
    """
    Genera un PDF vectorial tamaño US Letter (Vertical) con márgenes, columnas, renglones 
    y líneas verticales separadoras exactas en milímetros.
    """
    
    # El tamaño 'letter' por defecto ya es vertical (215.9 mm x 279.4 mm)
    ancho_pagina, alto_pagina = letter
    
    # Iniciar el canvas de ReportLab
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Configurar el grosor y color de la pluma
    c.setLineWidth(grosorDeBorde * mm)
    c.setStrokeColor(HexColor(colorDeGrosorDeBorde))
    
    # Calcular el área útil de la página restando los márgenes
    ancho_util = ancho_pagina - (2 * margenLateral * mm)
    alto_util = alto_pagina - (2 * margenVertical * mm)
    
    # Calcular el ancho exacto de cada columna
    ancho_columna = (ancho_util - (columnas - 1) * margenEntreColumnas * mm) / columnas
    
    # Dibujar la estructura por cada columna
    for col in range(columnas):
        # Coordenada X e Y de inicio de la columna actual
        x_start = (margenLateral * mm) + col * (ancho_columna + margenEntreColumnas * mm)
        y_start = margenVertical * mm
        
        # 1. Dibujar el borde contenedor de la columna
        c.rect(x_start, y_start, ancho_columna, alto_util)
        
        # 2. Dibujar línea vertical separadora (si NO es la última columna)
        if col < columnas - 1:
            # Se calcula la mitad del espacio entre columnas para centrar la línea
            x_linea_divisoria = x_start + ancho_columna + (margenEntreColumnas * mm / 2)
            c.line(x_linea_divisoria, y_start, x_linea_divisoria, y_start + alto_util)
        
        # 3. Dibujar los renglones internos de arriba hacia abajo
        y_actual = alto_pagina - (margenVertical * mm)
        
        while True:
            # Descontar el 'AltoDeLinea'
            y_actual -= (AltoDeLinea * mm)
            if y_actual <= y_start:
                break
            
            # Dibujar la línea principal
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)
            
            # Descontar el 'EspacioEntreLineas'
            y_actual -= (EspacioEntreLineas * mm)
            if y_actual <= y_start:
                break
            
            # Dibujar la línea secundaria (separador del espacio interlineal)
            c.line(x_start, y_actual, x_start + ancho_columna, y_actual)

    # Guardar y cerrar el documento
    c.save()
    return output_path

# Ejemplo de uso
if __name__ == "__main__":
    generar_pdf_columnas(
        margenLateral=10,
        margenVertical=10,
        margenEntreColumnas=20,
        columnas=3,
        grosorDeBorde=0.25,
        colorDeGrosorDeBorde='#eeeeee',
        AltoDeLinea=5,
        EspacioEntreLineas=4
    )