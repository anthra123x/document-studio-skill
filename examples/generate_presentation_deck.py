# -*- coding: utf-8 -*-
"""
Ejemplo de referencia: Generación de una presentación panorámica 16:9 con Document Studio.
Demuestra la creación directa de presentaciones sin scripts desechables.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from document_studio import Presentation, Diagram

# 1. Crear diagrama técnico de soporte (Zero AI-Slop)
diagram_path = "/tmp/diagrama_demo_deck.png"
Diagram.flow(
    title="PIPELINE DE PROCESAMIENTO ANALÍTICO",
    steps=[
        {"title": "Ingesta Kafka", "desc": "Eventos en streaming desde API Gateways", "color": "#38BDF8"},
        {"title": "Transformación", "desc": "Validación de esquemas y enriquecimiento", "color": "#818CF8"},
        {"title": "ClickHouse Cluster", "desc": "Indexación columnar y particionamiento mensual", "color": "#4ADE80"}
    ],
    output_png=diagram_path
)

# 2. Construir la presentación
deck = Presentation(title="Estrategia de Datos y Arquitectura Cloud 2026", theme="executive")

deck.add_slide(
    title="Arquitectura de Datos y Escalabilidad en la Nube",
    subtitle="Comité Técnico de Tecnología e Infraestructura",
    bullets=[
        "Evaluación de rendimiento y costos operativos en nubes híbridas.",
        "Resultados de las pruebas de carga sobre clusters analíticos.",
        "Hoja de ruta para la conmutación de producción sin interrupción de servicio."
    ],
    badge="VISIÓN GENERAL | SESIÓN TÉCNICA"
)

deck.add_slide(
    title="Flujo de Ingesta y Procesamiento Distribuido",
    subtitle="Topología de baja latencia con Kafka y ClickHouse",
    bullets=[
        "Latencia p95 reducida a 18.5 ms bajo cargas sostenidas de 14,800 QPS.",
        "Reducción del 34% en el costo mensual de infraestructura analítica.",
        "Cero tiempo de inactividad durante la sincronización dual de datos."
    ],
    badge="ARQUITECTURA | FLUJO END-TO-END",
    diagram_image_path=diagram_path
)

output_deck = "/tmp/presentacion_ejecutiva_demo.pptx"
success = deck.save(output_deck)

if success:
    sz = os.path.getsize(output_deck) / 1024
    print(f"✓ Presentación PPTX generada exitosamente: {output_deck} ({sz:.1f} KB)")
else:
    print("✗ Error al generar la presentación PPTX")

