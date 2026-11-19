# Document Studio

Suite y estándar de publicación editorial para la generación autónoma de **documentos en PDF** y **presentaciones panorámicas en PowerPoint (PPTX 16:9)** con alta densidad visual, control de saltos de página y cero dependencias pesadas.

---

## Filosofía de Diseño

1. **Cero Proliferación de Scripts Desechables:**  
   Proporciona una API en Python unificada (`Document`, `Presentation`, `Diagram`) para crear documentos completos en un único script de menos de 40 líneas.
2. **Cero Espaciados Muertos entre Páginas:**  
   Reglas calibradas de CSS Paged Media que evitan que tarjetas o tablas fuercen saltos de página prematuros dejando grandes espacios en blanco.
3. **Cero Ilustraciones IA Alucinadas (Zero AI-Slop):**  
   Motor de diagramas técnicos vectoriales limpios (4:3 y 16:9) renderizados a alta resolución.

---

## Instalación en Antigravity

La skill se encuentra enlazada al directorio global de configuración de Antigravity:

```bash
ln -s "/home/omicron/Documentos/document-studio" "$HOME/.gemini/config/skills/document-studio"
```

---

## Estructura del Repositorio

```
document-studio/
├── SKILL.md                          # Directiva técnica y reglas para el agente
├── README.md                         # Documentación general
├── .gitignore
├── document_studio/                  # Paquete Python autónomo
│   ├── __init__.py                   # Exportaciones principales: Document, Presentation, Diagram
│   ├── cli.py                        # Interfaz de línea de comandos (CLI)
│   ├── pdf/                          # Motor de documentos PDF
│   │   ├── builder.py                # Clase Document con API fluida
│   │   └── compiler.py               # Compilador headless multivehículo (Brave/Chromium/WeasyPrint)
│   ├── pptx/                         # Motor de presentaciones PPTX 16:9
│   │   └── builder.py                # Clase Presentation con manipulación OpenXML nativa
│   ├── diagrams/                     # Motor de diagramas vectoriales
│   │   └── generator.py              # Clase Diagram para flujos y arquitecturas
│   ├── themes/                       # Hojas de estilo y temas cromáticos
│   │   ├── base.css                  # CSS Paged Media (@page), cards, grids, tables
│   │   ├── executive.css             # Tema Corporativo (Navy/Slate/Gold)
│   │   ├── modern.css                # Tema High-Tech (Indigo/Zinc/Cyan)
│   │   ├── academic.css              # Tema Formal (Crimson/Serif)
│   │   └── minimal.css               # Tema Suizo de alta densidad (Monocromo)
│   └── templates/                    # Plantillas maestras
│       └── base_16_9.pptx            # Plantilla PPTX panorámica oficial
└── examples/                         # Ejemplos de uso de referencia
    ├── generate_executive_report.py  # Creación de un informe ejecutivo en 40 líneas
    └── generate_presentation_deck.py # Creación de diapositivas panorámicas
```

---

## Uso Rápido en Python

```python
from document_studio import Document

doc = Document(title="Resumen Trimestral", theme="executive")
doc.set_cover(title="Resumen Trimestral de Operaciones", author="Dirección General")
doc.add_kpis([
    {"value": "$4.2M", "label": "Ingresos Netos"},
    {"value": "+24%", "label": "Crecimiento Interanual"}
])
doc.add_section("1. Resultados Financieros")
doc.add_paragraph("Durante el presente ejercicio se consolidó la expansión regional...")
doc.render("balance.pdf")
```

