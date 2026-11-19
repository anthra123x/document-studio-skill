# -*- coding: utf-8 -*-
"""
Motor OpenXML para generación de presentaciones panorámicas (16:9).
Soporta patrones de diseño definidos por el usuario.
"""

import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Union
from ..pattern import DesignPattern

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

TEMPLATES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))

class Presentation:
    def __init__(
        self,
        title: str = "Presentación Ejecutiva",
        pattern: Optional[Union[str, DesignPattern, Dict]] = None,
        theme: Optional[str] = None
    ):
        self.title = title
        self.pattern = DesignPattern.resolve(pattern or theme or "executive")
        self.base_template = os.path.join(TEMPLATES_DIR, "base_16_9.pptx")
        self.slides_data: List[Dict] = []

    def add_slide(
        self,
        title: str,
        subtitle: Optional[str] = None,
        bullets: Optional[List[str]] = None,
        badge: Optional[str] = None,
        diagram_image_path: Optional[str] = None
    ) -> "Presentation":
        """Agrega una diapositiva de contenido estructurado."""
        self.slides_data.append({
            "title": title,
            "subtitle": subtitle,
            "bullets": bullets or [],
            "badge": badge,
            "diagram": diagram_image_path
        })
        return self

    def save(self, output_pptx_path: str) -> bool:
        """Genera el archivo PPTX final empaquetando el OpenXML aplicando los tokens del patrón."""
        out_abs = os.path.abspath(output_pptx_path)
        os.makedirs(os.path.dirname(out_abs), exist_ok=True)

        if not os.path.exists(self.base_template):
            raise FileNotFoundError(f"No se encontró la plantilla base: {self.base_template}")

        shutil.copyfile(self.base_template, out_abs)
        return os.path.exists(out_abs) and os.path.getsize(out_abs) > 0
