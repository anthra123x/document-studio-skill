# Document Studio: Suite de Diseno Editorial y Publicacion para Agentes de IA

`document-studio` es una suite y estandar de publicacion editorial para agentes de inteligencia artificial y desarrolladores de software. Su objetivo primordial es permitir la generacion autonoma, determinista y directa de documentos tecnicos en formato PDF y presentaciones panoramicas en formato PowerPoint (PPTX 16:9), eliminando la necesidad de scripts auxiliares desechables, evitando espaciados muertos entre paginas y erradicando ilustraciones alucinadas («AI-slop»).

El proyecto opera bajo un modelo dual:
1. **Skill de Agente (Agent Skill):** Expuesta mediante la especificacion `SKILL.md` para ser consumida directamente por entornos de ejecucion como Google Antigravity, Claude Code y arquitecturas multi-agente.
2. **Biblioteca de Python Autonoma (`document_studio`):** Motor modular que implementa composicion basada en CSS Paged Media, manipulacion nativa de esquemas OpenXML y renderizado de diagramas vectoriales de alta resolucion.

---

## 1. Principios de Diseno Editorial

### 1.1. Cero Proliferacion de Scripts Desechables
Los agentes de IA convencionales suelen generar cadenas de archivos temporales (`temp.html`, `make_part1.py`, `convert.sh`) propensos a fallos de entorno. Document Studio encapsula todo el ciclo de vida en una API fluida en Python que permite construir, maquetar y compilar un documento completo en menos de 40 lineas dentro de un unico bloque de ejecucion.

### 1.2. Paginacion Estricta y Supresion de Espacios Muertos (Zero-Gap)
El mayor problema al compilar HTML a PDF radica en saltos de pagina descontrolados generados por reglas CSS mal aplicadas:
- **Restriccion de `break-inside: avoid`:** La directiva `break-inside: avoid` (o `page-break-inside: avoid`) se restringe de manera estricta a nodos atomicos hoja (`.card`, `.kpi-box`, `.callout`, `tr`, `pre`). Esta prohibido aplicarla a secciones, articulos o contenedores de bloque principales, previniendo que bloques voluminosos sean empujados a la siguiente pagina dejando la anterior a medio llenar.
- **Supresion de Encabezados Huerfanos:** Todos los titulos (`h1`, `h2`, `h3`, `h4`) imponen `break-after: avoid !important` para impedir que un encabezado quede al final de una pagina desvinculado de su parrafo siguiente.
- **Geometria Calibrada:** Margenes estandarizados de 14 mm para tamano Carta (Letter) y A4, maximizando el area util de contenido y reduciendo el consumo de papel o paginas innecesarias.

### 1.3. Cero Ilustraciones Alucinadas (Zero AI-Slop)
En lugar de depender de modelos generativos de difusion para ilustrar documentos tecnicos (los cuales suelen distorsionar texto y diagramas), Document Studio incorpora un motor de diagramas tecnicos vectoriales (`Diagram`) que genera flujos de datos y diagramas de arquitectura en alta resolucion (1200x900 y 1920x1080) mediante HTML5/CSS Grid renderizado de forma determinista.

### 1.4. Sistema de Patrones de Diseno Centrado en el Usuario (User-Driven Design Pattern)
La apariencia visual se desacopla del contenido mediante la clase `DesignPattern`. El usuario o el agente pueden definir paletas de colores corporativas, tipografias y margenes mediante presets o diccionarios de tokens, y el motor propaga automaticamente estos atributos tanto a las hojas de estilo del PDF como a las capas XML de la presentacion PPTX.

---

## 2. Mapa de Modulos

De acuerdo con el estandar arquitectonico del proyecto, cada modulo posee su propia especificacion y memoria viva local (`README.agent.md`).

| Modulo | Ruta | Responsabilidad Tecnica | Documentacion Local |
| :--- | :--- | :--- | :--- |
| **Nucleo Document Studio** | `document_studio/` | Fachada principal, versionado, API publica y CLI de entrada | [README.agent.md](file:///home/omicron/Documentos/document-studio/document_studio/README.agent.md) |
| **Motor PDF** | `document_studio/pdf/` | Builder fluido de documentos y compilador headless multivehiculo | [README.agent.md](file:///home/omicron/Documentos/document-studio/document_studio/pdf/README.agent.md) |
| **Motor PPTX** | `document_studio/pptx/` | Ensamblador de presentaciones panoramicas 16:9 basado en OpenXML | [README.agent.md](file:///home/omicron/Documentos/document-studio/document_studio/pptx/README.agent.md) |
| **Motor de Diagramas** | `document_studio/diagrams/` | Renderizador vectorial de diagramas tecnicos en alta resolucion | [README.agent.md](file:///home/omicron/Documentos/document-studio/document_studio/diagrams/README.agent.md) |
| **Motor de Patrones** | `document_studio/pattern.py` | Definicion de tokens visuales, resolucion de estilos y presets | Integrado en nucleo |
| **Hojas de Estilo** | `document_studio/themes/` | CSS Paged Media base, reset editorial y temas cromatics | [README.agent.md](file:///home/omicron/Documentos/document-studio/document_studio/themes/README.agent.md) |
| **Plantillas Base** | `document_studio/templates/` | Plantilla OpenXML maestra `base_16_9.pptx` | Almacen estatico |
| **Ejemplos de Referencia** | `examples/` | Implementaciones completas y verificables de casos de uso | [README.agent.md](file:///home/omicron/Documentos/document-studio/examples/README.agent.md) |

---

## 3. Instalacion y Requisitos del Sistema

### 3.1. Requisitos de Ejecucion
- Python 3.8 o superior.
- Al menos uno de los siguientes motores headless instalados en el entorno (detectados automaticamente en tiempo de ejecucion por `find_headless_engine`):
  - Brave Browser (`brave` o `brave-browser`)
  - Chromium (`chromium` o `chromium-browser`)
  - Google Chrome (`google-chrome` o `google-chrome-stable`)
  - WeasyPrint (binario CLI o paquete Python `weasyprint`)

### 3.2. Instalacion como Skill de Agente (Antigravity / Claude Code)
Para registrar la skill en el entorno del agente, crear un enlace simbolico al directorio de skills:

```bash
# Para Antigravity
ln -s "$(pwd)" "$HOME/.gemini/config/skills/document-studio"

# Para Claude Code
ln -s "$(pwd)" "$HOME/.claude/skills/document-studio"
```

### 3.3. Uso como Biblioteca en Entornos de Desarrollo
El modulo puede agregarse directamente al `PYTHONPATH` o importarse de forma relativa dentro de cualquier proyecto:

```bash
export PYTHONPATH="${PYTHONPATH}:/ruta/a/document-studio"
```

---

## 4. Referencia de la API de Python

### 4.1. Clase `Document` (`document_studio.pdf.builder`)
Orquesta la generacion de documentos PDF estructurados.

#### Constructor:
```python
Document(
    title: str = "Documento",
    category: str = "DOCUMENTO TECNICO",
    pattern: Optional[Union[str, DesignPattern, Dict]] = None,
    theme: Optional[str] = None,
    size: str = "letter",
    running_title: Optional[str] = None,
    footer_note: Optional[str] = None
)
```

#### Metodos Principales:
- `set_cover(title, subtitle=None, author=None, organization=None, date=None, category=None) -> Document`: Configura una portada compacta integrada sin generar hojas en blanco forzadas.
- `add_section(title: str) -> Document`: Anade un encabezado de seccion principal (`h2`) con proteccion contra desbordamiento.
- `add_paragraph(text: str) -> Document`: Anade un parrafo tipografico con alineacion justificada y espaciado calibrado.
- `add_kpis(kpis: List[Dict[str, str]]) -> Document`: Genera una cuadricula responsiva de indicadores clave (KPIs). Cada elemento es un diccionario con `value` y `label`.
- `add_card(title: str, content: str) -> Document`: Genera una tarjeta de contenido con borde sutil y fondo neutral.
- `add_callout(title: str, text: str, kind: str = "info") -> Document`: Anade un bloque destacado. `kind` admite `'info'`, `'success'`, `'warning'` y `'danger'`.
- `add_table(headers: List[str], rows: List[List[str]]) -> Document`: Inserta una tabla con diseno editorial, encabezados destacados y filas alternas protegidas contra cortes de pagina intermedios.
- `add_image(image_path: str, caption: Optional[str] = None, width: str = "100%") -> Document`: Inserta un grafico o diagrama con su pie de figura.
- `add_raw_html(html: str) -> Document`: Permite la inyeccion directa de marcado HTML cuando se requiere una estructura personalizada.
- `render(output_pdf_path: str) -> bool`: Compila el documento final a la ruta especificada. Retorna `True` si el archivo se genera con exito.

---

### 4.2. Clase `Presentation` (`document_studio.pptx.builder`)
Gestiona la creacion de presentaciones panoramicas 16:9 modificando paquetes OpenXML nativos.

#### Constructor:
```python
Presentation(
    title: str = "Presentacion Ejecutiva",
    pattern: Optional[Union[str, DesignPattern, Dict]] = None,
    theme: Optional[str] = None
)
```

#### Metodos Principales:
- `add_slide(title: str, subtitle: Optional[str] = None, bullets: Optional[List[str]] = None, badge: Optional[str] = None, diagram_image_path: Optional[str] = None) -> Presentation`: Agrega una diapositiva estruturada. Soporta badges de orador o categoria, listas de puntos clave y diagrama tecnico lateral.
- `save(output_pptx_path: str) -> bool`: Empaqueta la presentacion final en formato `.pptx`.

---

### 4.3. Clase `Diagram` (`document_studio.diagrams.generator`)
Genera diagramas tecnicos vectoriales sin dependencias de servicios externos.

#### Metodos Estaticos:
- `Diagram.flow(title: str, steps: List[Dict[str, str]], output_png: str, width: int = 1200, height: int = 900) -> bool`: Genera un diagrama de flujo horizontal o vertical con bloques secuenciales definidos por `title`, `desc` y `color`.
- `Diagram.architecture(title: str, layers: List[Dict[str, Any]], output_png: str, width: int = 1200, height: int = 900) -> bool`: Genera un diagrama de capas o modulos de software.
- `Diagram.render_html(html_body: str, output_png_path: str, width: int = 1200, height: int = 900) -> bool`: Renderiza cualquier marcado HTML5/CSS Grid a una imagen PNG de alta densidad mediante el navegador headless.

---

### 4.4. Clase `DesignPattern` (`document_studio.pattern`)
Representa la especificacion de tokens visuales y presets del sistema.

#### Presets Disponibles:
- `executive`: Diseno corporativo clasico (Azul marino `#1E3A8A`, Pizarra `#0F172A`, Acentos dorados `#D97706`).
- `modern`: Diseno de ingenieria y software (Indigo `#4F46E5`, Acentos cian `#06B6D4`, Fondo `#F9FAFB`).
- `academic_ufps`: Diseno formal universitario (Rojo UFPS `#C8102E`, Cian `#38BDF8`, notas de pie institucionales).
- `minimal`: Diseno suizo de maxima densidad tipografica (Monocromo `#000000`, escala de grises neutra).
- `dark`: Diseno oscuro tecnico para especificaciones de ciberseguridad o infraestructura (Fondo `#0F172A`, texto `#F8FAFC`, acentos cian y esmeralda).

#### Resolucion Dinamica:
```python
from document_studio import DesignPattern

# Resolucion por nombre
patron = DesignPattern.resolve("modern")

# Resolucion por parametros personalizados
patron_custom = DesignPattern(
    name="Fintech Cloud",
    primary_color="#0A2540",
    secondary_color="#635BFF",
    accent_color="#00D4FF",
    page_size="letter"
)
```

---

## 5. Ejemplos de Implementacion

### 5.1. Generacion de Informe Tecnico en PDF (Ejecutable)
```python
from document_studio import Document

doc = Document(
    title="Evaluacion de Rendimiento de Base de Datos",
    category="INFORME DE INGENIERIA",
    pattern="modern",
    running_title="AUDITORIA TECNICA 2026"
)

# Portada integrada
doc.set_cover(
    title="Evaluacion de Rendimiento de Base de Datos",
    subtitle="Comparativa de latencia en consultas analiticas sobre ClickHouse y PostgreSQL",
    author="Equipo de Datos",
    organization="Direccion de Ingenieria",
    date="Noviembre 2026"
)

# Seccion de metricas clave
doc.add_kpis([
    {"value": "18.5 ms", "label": "Latencia p95"},
    {"value": "14.8K req/s", "label": "Capacidad Maxima"},
    {"value": "99.99%", "label": "Disponibilidad SLA"},
    {"value": "-42%", "label": "Consumo de RAM"}
])

# Seccion estructurada
doc.add_section("1. Analisis Operativo")
doc.add_paragraph(
    "Las pruebas de estres demostraron que el motor columnar mantiene tiempos de respuesta estables "
    "bajo cargas concurrentes intensas, evitando degradacion en transacciones criticas."
)

doc.add_callout(
    "Recomendacion de Despliegue",
    "Configurar politicas de compresion LZ4 en tablas particionadas por fecha para optimizar espacio.",
    kind="warning"
)

# Tabulacion de datos
doc.add_table(
    headers=["Motor", "Instancias", "Latencia Media", "Consumo CPU", "Estado"],
    rows=[
        ["ClickHouse 24.8", "3 nodos", "18.5 ms", "28%", "Optimo"],
        ["PostgreSQL 16", "1 primario / 2 replicas", "74.2 ms", "64%", "Estable"]
    ]
)

# Compilacion directa
doc.render("informe_rendimiento.pdf")
```

### 5.2. Generacion de Presentacion Panorama 16:9 con Diagrama Vectorial
```python
from document_studio import Presentation, Diagram

# 1. Renderizado de diagrama de arquitectura
diagram_path = "pipeline_datos.png"
Diagram.flow(
    title="FLUJO DE PROCESAMIENTO ANALITICO",
    steps=[
        {"title": "Ingesta", "desc": "Kafka Streaming a 50k msg/s", "color": "#38BDF8"},
        {"title": "Transformacion", "desc": "Filtrado y enriquecimiento", "color": "#818CF8"},
        {"title": "Persistencia", "desc": "Almacenamiento en ClickHouse", "color": "#4ADE80"}
    ],
    output_png=diagram_path
)

# 2. Ensamblado de diapositivas
deck = Presentation(title="Estrategia de Ingenieria 2026", pattern="executive")

deck.add_slide(
    title="Arquitectura de Datos y Escalabilidad",
    subtitle="Resultados de la evaluacion trimestral de infraestructura",
    bullets=[
        "Reduccion de latencia p95 a menos de 20 ms bajo concurrencia alta.",
        "Ahorro neto del 34% en costes mensuales de almacenamiento.",
        "Compatibilidad nativa con herramientas de observabilidad OpenTelemetry."
    ],
    badge="INGENIERIA | ARQUITECTURA",
    diagram_image_path=diagram_path
)

deck.save("presentacion_arquitectura.pptx")
```

---

## 6. Interfaz de Linea de Comandos (CLI)

Document Studio incluye una herramienta CLI para compilar archivos HTML existentes o crear informes ejecutivos basicos:

### 6.1. Compilacion de un archivo HTML:
```bash
python3 -m document_studio.cli compile entrada.html salida.pdf --size letter
```

### 6.2. Creacion rapida de un informe ejecutivo:
```bash
python3 -m document_studio.cli quick-report \
  --title "Resumen de Estado Operativo" \
  --output "resumen_operativo.pdf" \
  --theme modern \
  --author "Departamento de Infraestructura"
```

---

## 7. Protocolo de Verificacion y Calidad Pre-Entrega

Antes de finalizar la entrega de cualquier documento o presentacion generada por la skill, se deben verificar los siguientes puntos:

1. **Auditoria de Paginacion:**
   Ejecutar `pdfinfo documento.pdf` y verificar que el numero total de paginas coincida con el volumen real de datos. No deben existir paginas huerfanas ni hojas en blanco al final.
2. **Auditoria de Espaciado:**
   Comprobar visualmente o mediante analisis de cajas que ningun bloque deje vacios superiores a un tercio de pagina antes de una tabla o seccion.
3. **Auditoria de Contraste Tipografico:**
   Asegurar que los contrastes de color cumplan con estandares de legibilidad minima: texto sobre fondos oscuros debe utilizar tonos claros (`#F8FAFC`); texto sobre fondos claros debe utilizar tonos oscuros (`#0F172A`).
4. **Verificacion de Dependencias:**
   Certificar que la compilacion se ejecute con modulos estandar y motores headless ya presentes en el sistema anfitrion.
