# -*- coding: utf-8 -*-
"""
Ejemplo de referencia: Generación de un informe ejecutivo completo en menos de 40 líneas de código.
Demuestra la ausencia total de archivos intermedios o scripts desechables.
"""

import os
import sys

# Permitir importación directa desde el repositorio local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from document_studio import Document

doc = Document(
    title="Evaluación de Arquitectura de Datos y Escalabilidad en la Nube",
    category="INFORME DE INGENIERÍA",
    theme="executive",
    size="letter",
    running_title="INFORME ARQUITECTURA CLOUD 2026",
    footer_note="Confidencial · Dirección de Tecnología"
)

# Portada compacta sin páginas vacías
doc.set_cover(
    title="Evaluación de Arquitectura de Datos y Escalabilidad en la Nube",
    subtitle="Análisis comparativo de persistencia columnar, rendimiento de consultas analíticas y costos operativos en AWS vs GCP",
    author="Comité Técnico de Arquitectura",
    organization="Plataforma de Ingeniería & Analítica",
    date="Noviembre 2026"
)

# Métricas clave en una sola línea
doc.add_kpis([
    {"value": "1.2 TB/día", "label": "Volumen de Ingesta"},
    {"value": "18.5 ms", "label": "Latencia p95"},
    {"value": "99.99%", "label": "Disponibilidad SLA"},
    {"value": "-34%", "label": "Reducción de Costos"}
])

doc.add_section("1. Resumen Ejecutivo")
doc.add_paragraph(
    "Durante el último trimestre, se evaluó la migración del pipeline analítico central hacia una arquitectura basada en ClickHouse y Apache Kafka. "
    "Los resultados demuestran una mejora sustancial en tiempos de respuesta de consultas complejas sobre series temporales, reduciendo el consumo de memoria en un 42%."
)

doc.add_callout(
    "Hallazgo Crítico",
    "La compresión de columnas LZ4 junto con esquemas particionados por mes redujo el almacenamiento requerido de 45 TB a 14.8 TB efectivos.",
    kind="success"
)

doc.add_section("2. Comparativa de Rendimiento por Motor")
doc.add_table(
    headers=["Motor Evaluado", "Consultas/seg (QPS)", "Latencia Media", "Consumo RAM", "Costo Mensual Estimado"],
    rows=[
        ["PostgreSQL (Timescale)", "1,250", "145 ms", "32 GB", "$1,450 USD"],
        ["Google BigQuery", "N/A (Serverless)", "850 ms", "Bajo demanda", "$2,100 USD"],
        ["ClickHouse Cloud (HNSW)", "14,800", "18.5 ms", "16 GB", "$780 USD"],
        ["Amazon Redshift Serverless", "3,400", "320 ms", "Bajo demanda", "$2,400 USD"]
    ]
)

doc.add_section("3. Conclusiones y Plan de Implementación")
doc.add_columns([
    """
    <div class="card">
        <div class="card-title">Fase 1: Ingesta Dual (Semanas 1-4)</div>
        <p>Duplicación controlada del flujo Kafka hacia el nuevo cluster sin afectar los dashboards analíticos de producción.</p>
    </div>
    """,
    """
    <div class="card">
        <div class="card-title">Fase 2: Conmutación Definitiva (Semanas 5-6)</div>
        <p>Redirección total de endpoints de consulta GraphQL hacia ClickHouse y desmantelamiento de instancias legadas.</p>
    </div>
    """
])

output_file = "/tmp/informe_ejecutivo_demo.pdf"
success = doc.render(output_file)
if success:
    sz = os.path.getsize(output_file) / 1024
    print(f"✓ Documento PDF generado exitosamente: {output_file} ({sz:.1f} KB)")
else:
    print("✗ Error al generar el documento PDF")
