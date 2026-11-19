# -*- coding: utf-8 -*-
"""
Document Studio: Suite integral de publicación, diseño editorial y generación de documentos y presentaciones.
"""

from .pdf.builder import Document
from .pptx.builder import Presentation
from .diagrams.generator import Diagram
from .pdf.compiler import compile_pdf
from .pattern import DesignPattern

__version__ = "1.1.0"
__all__ = ["Document", "Presentation", "Diagram", "compile_pdf", "DesignPattern"]
