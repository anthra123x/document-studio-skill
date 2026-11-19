---
name: document-studio
description: >-
  Suite y estándar de diseño editorial para la generación directa de documentos (PDF)
  y presentaciones panorámicas 16:9 (PPTX) con maquetación profesional, densidad visual calibrada,
  eliminación de espaciados muertos entre páginas y generación autónoma en una sola pasada
  sin crear scripts auxiliares desechables.
---

# Document Studio: Suite de Publicación Editorial y Presentaciones

`document-studio` es el estándar y motor de publicación del agente para generar **documentos en PDF** y **presentaciones en PowerPoint (PPTX)** de alta fidelidad técnica y estética editorial.

El propósito central de esta skill es **eliminar la proliferación de scripts intermedios y archivos desechables**: proporciona una API unificada en Python (`Document`, `Presentation`, `Diagram`) y un sistema de estilos CSS Paged Media que resuelve automáticamente la paginación, la supresión de espacios en blanco y el contraste.

---

## 1. Cuándo Activar esta Skill

Activa esta skill inmediatamente cuando el usuario pida:
- Crear o maquetar **informes técnicos, reportes ejecutivos, balances, whitepapers o especificaciones de arquitectura en PDF**.
- Generar **artículos de investigación o papers** con formato riguroso (IEEE, APA, ACM) y citas en sangría francesa.
- Crear **cheat sheets, solucionarios, hojas de referencia o resúmenes de estudio** de alta densidad visual.
- Diseñar **presentaciones panorámicas en PowerPoint (PPTX 16:9)** con diapositivas limpias, badges y diagramas técnicos.
- Cuando se requiera exportar o compilar documentos **sin dejar páginas vacías, sin cabeceras huérfanas y sin saltos incómodos**.

---

## 2. Los Dos Mandamientos Editoriales (Zero-Slop & Zero-Gap)

1. **Cero Espaciados Muertos ni Páginas Vacías:**
   - La regla CSS `page-break-inside: avoid` (o `break-inside: avoid`) se aplica **únicamente a elementos atómicos** (`.card`, `.kpi-box`, `.callout`, filas de tabla, bloques de código `pre`). **PROHIBIDO** aplicarla a contenedores grandes o secciones enteras, ya que esto empuja bloques grandes a la siguiente página dejando media página en blanco.
   - Todos los encabezados (`h1`, `h2`, `h3`, `h4`) llevan `break-after: avoid !important` para impedir que un título quede al final de una página sin su texto correspondiente.
   - Márgenes calibrados de página: `margin: 14mm` para Letter/A4, maximizando el área útil sin saturar los bordes.

2. **Cero Proliferación de Archivos Temporales:**
   - No crees múltiples scripts `make_part1.py`, `make_part2.py`, `temp.html` dispersos en el proyecto.
   - Utiliza la clase `Document` o `Presentation` directamente desde Python en un único archivo o script limpio de ejecución.

---

## 3. Generación de Documentos PDF en 15 Líneas de Código

No escribas HTML crudo desde cero si no es necesario. Usa la API fluida de `document_studio`:

```python
from document_studio import Document

# 1. Instanciar documento con tema ('executive', 'modern', 'academic', 'minimal')
doc = Document(
    title="Evaluación de Arquitectura de Microservicios",
    category="INFORME DE INGENIERÍA",
    theme="executive", # o 'modern', 'academic', 'minimal'
    size="letter",     # o 'a4'
    running_title="AUDITORÍA DE INFRAESTRUCTURA 2026",
    footer_note="Confidencial · Uso Interno"
)

# 2. Portada compacta integrada (no genera páginas en blanco innecesarias)
doc.set_cover(
    title="Evaluación de Arquitectura de Microservicios",
    subtitle="Análisis de latencia, concurrencia y costos operativos en Kubernetes",
    author="Equipo de Arquitectura Cloud",
    organization="Dirección de Tecnología",
    date="Noviembre 2026"
)

# 3. Métricas clave (KPIs) en 2, 3 o 4 columnas
doc.add_kpis([
    {"value": "99.99%", "label": "Disponibilidad"},
    {"value": "18.5 ms", "label": "Latencia p95"},
    {"value": "14.8K req/s", "label": "Rendimiento"},
    {"value": "-34%", "label": "Ahorro de Costos"}
])

# 4. Secciones y párrafos con tipografía justificada
doc.add_section("1. Resumen Ejecutivo")
doc.add_paragraph("Este informe resume los hallazgos tras la migración a clusters distribuidos...")

# 5. Callouts semánticos ('info', 'success', 'warning', 'danger')
doc.add_callout("Recomendación Crítica", "Habilitar mTLS en todos los enlaces inter-servicio.", kind="warning")

# 6. Tablas con diseño editorial compacto
doc.add_table(
    headers=["Servicio", "Instancias", "CPU Media", "Memoria", "Estado"],
    rows=[
        ["Auth Gateway", "4 pods", "24%", "512 MB", "Estable"],
        ["Billing API", "6 pods", "38%", "1024 MB", "Estable"],
        ["Data Pipeline", "8 pods", "62%", "2048 MB", "Carga Alta"]
    ]
)

# 7. Columnas paralelas para conclusiones o tarjetas
doc.add_columns([
    "<div class='card'><div class='card-title'>Ventajas</div><p>Escalabilidad horizontal desacoplada.</p></div>",
    "<div class='card'><div class='card-title'>Riesgos</div><p>Mayor complejidad en observabilidad.</p></div>"
])

# 8. Renderizar directamente al PDF final
doc.render("reporte_final.pdf")
```

---

## 4. Temas Disponibles

| Tema | Clave | Paleta Primaria | Estilo Tipográfico | Recomendado Para |
| :--- | :---: | :--- | :--- | :--- |
| **Executive** | `executive` | Deep Navy (`#1E3A8A`), Slate, Oro (`#D97706`) | Sans-serif sobrio y corporativo | Informes directivos, auditorías, finanzas. |
| **Modern Tech** | `modern` | Indigo (`#4F46E5`), Zinc, Cian | Tipografía moderna de alta legibilidad | Documentación de software, whitepapers, APIs. |
| **Academic** | `academic` | Carmesí (`#991B1B`), Slate, Blanco | Serif formal en cuerpo, sans en títulos | Tesis, artículos científicos, guías de estudio. |
| **Minimal** | `minimal` | Monocromático Negro/Blanco (`#000000`) | Suiza internacional de alta densidad | Cheat sheets, especificaciones, diagramas. |

---

## 5. Generación de Presentaciones Panorámicas (PPTX 16:9)

Para crear diapositivas limpias con badges de contexto y cero texto de bajo contraste:

```python
from document_studio import Presentation, Diagram

# 1. Crear diagrama vectorial si la diapositiva lo amerita
diagram_file = "assets/flujo_datos.png"
Diagram.flow(
    title="PIPELINE DE INGESTA",
    steps=[
        {"title": "Captura", "desc": "Ingesta en streaming con Kafka", "color": "#38BDF8"},
        {"title": "Validación", "desc": "Filtrado y validación de esquemas", "color": "#818CF8"},
        {"title": "Persistencia", "desc": "Almacenamiento columnar en ClickHouse", "color": "#4ADE80"}
    ],
    output_png=diagram_file
)

# 2. Construir la presentación
deck = Presentation(title="Estrategia Cloud 2026", theme="executive")

deck.add_slide(
    title="Arquitectura de Datos y Escalabilidad",
    subtitle="Evaluación de rendimiento en plataformas híbridas",
    bullets=[
        "Reducción de latencia a 18.5 ms bajo cargas sostenidas de 14,800 QPS.",
        "Ahorro del 34% en el costo mensual de infraestructura analítica.",
        "Cero tiempo de inactividad durante la migración de esquemas."
    ],
    badge="INGENIERÍA | SESIÓN TÉCNICA",
    diagram_image_path=diagram_file
)

deck.save("presentacion_final.pptx")
```

---

## 6. Motor de Compilación Headless (CLI y Script)

El compilador de `document_studio` detecta automáticamente el binario disponible en el entorno (`brave`, `chromium`, `google-chrome` o `weasyprint`) y aplica las banderas de compilación estricta:
- `--no-pdf-header-footer` (elimina cabeceras residuales con URLs o fechas del navegador).
- `--run-all-compositor-stages-before-draw` (garantiza renderizado total de vectores y fuentes web).

Desde la terminal:
```bash
python3 -m document_studio.cli compile entrada.html salida.pdf
```
O generación rápida:
```bash
python3 -m document_studio.cli quick-report --title "Balance Trimestral" --output balance.pdf --theme executive
```

---

## 7. Checklist de Calidad Pre-Entrega

Antes de entregar cualquier documento o presentación al usuario:
- [ ] **Auditoría de Páginas:** Ejecuta `pdfinfo documento.pdf` y verifica que el número de páginas corresponda exactamente al volumen de contenido, sin páginas blancas residuales al final.
- [ ] **Auditoría de Separaciones:** Asegúrate de que las secciones principales no dejen vacíos desproporcionados.
- [ ] **Auditoría de Contraste:** Todo texto sobre fondo oscuro debe ser claro (`#F8FAFC`); todo texto sobre fondo claro debe ser oscuro (`#0F172A` o `#1E293B`).
- [ ] **Auditoría de Dependencias:** El script de generación no debe depender de paquetes no instalados; utiliza los módulos nativos incluidos en `document_studio`.
