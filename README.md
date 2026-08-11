# Formatted Sheet Generator

Generador de hojas PDF vectoriales con cuadrícula de columnas y renglones, pensado para imprimir plantillas en blanco (notas, listas, formularios manuscritos, etc.).

El proyecto usa [ReportLab](https://www.reportlab.com/) para dibujar líneas y bordes con precisión en milímetros sobre papel tamaño **US Letter** (215.9 × 279.4 mm, orientación vertical).

## Características

- **PDF vectorial** — Las líneas se escalan sin pérdida de calidad al imprimir.
- **Medidas en milímetros** — Márgenes, columnas, renglones y separadores configurables con precisión.
- **Columnas múltiples** — De 1 a N columnas con espacio configurable entre ellas.
- **Renglones dobles** — Cada fila incluye una línea principal y una secundaria para simular espacio interlineal (útil para escritura a mano).
- **Separadores verticales** — Líneas centradas en el espacio entre columnas.
- **Personalizable** — Grosor y color del trazo, altura de línea y espacio entre líneas.

## Requisitos

- Python 3.8 o superior
- [ReportLab](https://pypi.org/project/reportlab/) ≥ 4.0

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/EduardoOsteicoechea/formatted_sheet_generator.git
cd formatted_sheet_generator

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (CMD):
.\.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso rápido

Ejecutar el script con los valores por defecto del ejemplo:

```bash
python app.py
```

Esto genera `documento_generado.pdf` en el directorio actual.

## Uso como módulo

```python
from app import generar_pdf_columnas

generar_pdf_columnas(
    margenLateral=10,
    margenVertical=10,
    margenEntreColumnas=20,
    columnas=3,
    grosorDeBorde=0.25,
    colorDeGrosorDeBorde='#eeeeee',
    AltoDeLinea=5,
    EspacioEntreLineas=4,
    output_path='mi_hoja.pdf'
)
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `margenLateral` | `float` | `20` | Margen izquierdo y derecho de la página, en mm. |
| `margenVertical` | `float` | `10` | Margen superior e inferior de la página, en mm. |
| `margenEntreColumnas` | `float` | `20` | Espacio horizontal entre columnas, en mm. La línea separadora se dibuja en el centro de este espacio. |
| `columnas` | `int` | `3` | Número de columnas en la hoja. |
| `grosorDeBorde` | `float` | `0.25` | Grosor del trazo de todas las líneas, en mm. |
| `colorDeGrosorDeBorde` | `str` | `'#eeeeee'` | Color del trazo en formato hexadecimal (`#RRGGBB`). |
| `AltoDeLinea` | `float` | `5` | Altura de cada renglón principal, en mm. |
| `EspacioEntreLineas` | `float` | `4` | Espacio adicional entre renglones (línea secundaria), en mm. |
| `output_path` | `str` | `'documento_generado.pdf'` | Ruta del archivo PDF de salida. |

## Cómo se construye la hoja

1. Se calcula el **área útil** restando los márgenes laterales y verticales del tamaño Letter.
2. El ancho de cada columna se reparte equitativamente, descontando los espacios entre columnas.
3. Por cada columna se dibuja:
   - Un **rectángulo contenedor** (borde exterior).
   - Una **línea vertical separadora** centrada en el espacio hacia la siguiente columna (excepto en la última).
   - **Renglones horizontales** de arriba hacia abajo: línea principal → espacio → línea secundaria → repetir hasta llenar la columna.

```
┌──────────────┐   │   ┌──────────────┐   │   ┌──────────────┐
│ ──────────── │   │   │ ──────────── │   │   │ ──────────── │
│ ─ ─ ─ ─ ─ ─  │   │   │ ─ ─ ─ ─ ─ ─  │   │   │ ─ ─ ─ ─ ─ ─  │
│ ──────────── │   │   │ ──────────── │   │   │ ──────────── │
│     ...      │   │   │     ...      │   │   │     ...      │
└──────────────┘   │   └──────────────┘   │   └──────────────┘
     columna 1     │      columna 2     │      columna 3
```

## Ejemplos de configuración

**Cuaderno de una sola columna (tipo carta):**

```python
generar_pdf_columnas(columnas=1, margenLateral=15, AltoDeLinea=7, EspacioEntreLineas=3)
```

**Hoja tipo periódico (4 columnas estrechas):**

```python
generar_pdf_columnas(columnas=4, margenEntreColumnas=8, margenLateral=12, AltoDeLinea=4)
```

**Líneas más visibles para impresión en blanco y negro:**

```python
generar_pdf_columnas(grosorDeBorde=0.4, colorDeGrosorDeBorde='#cccccc')
```

## Estructura del proyecto

```
formatted_sheet_generator/
├── app.py              # Lógica de generación del PDF
├── requirements.txt    # Dependencias de Python
├── README.md           # Este archivo
└── LICENSE             # Licencia MIT
```

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Copyright (c) 2026 Eduardo.

## Autor

[EduardoOsteicoechea](https://github.com/EduardoOsteicoechea)
