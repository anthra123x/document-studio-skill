# -*- coding: utf-8 -*-
"""
Motor de compilación PDF de alta velocidad y precisión tipográfica.
Detecta automáticamente el navegador headless o WeasyPrint disponible en el entorno.
"""

import os
import sys
import shutil
import tempfile
import subprocess
from typing import Optional

def find_headless_engine() -> tuple[Optional[str], str]:
    """
    Detecta el mejor motor disponible en el sistema.
    Retorna (ruta_binario, tipo_motor: 'chromium' | 'weasyprint').
    """
    for candidate in ["brave", "brave-browser", "chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]:
        path = shutil.which(candidate)
        if path:
            return path, "chromium"

    if shutil.which("weasyprint"):
        return shutil.which("weasyprint"), "weasyprint"

    # Verificar si el módulo WeasyPrint de Python está instalado
    try:
        import weasyprint
        return "python_module", "weasyprint"
    except ImportError:
        pass

    return None, "none"

def compile_pdf(
    html_source: str,
    output_pdf_path: str,
    is_file: bool = False,
    page_size: str = "letter",
    landscape: bool = False
) -> bool:
    """
    Compila contenido HTML a un documento PDF optimizado.
    
    Args:
        html_source: Ruta al archivo HTML o cadena con código HTML completo.
        output_pdf_path: Ruta destino donde se guardará el PDF.
        is_file: True si html_source es una ruta existente, False si es código HTML.
        page_size: 'letter' o 'a4'.
        landscape: True para orientación horizontal.
    
    Returns:
        True si el archivo PDF fue generado exitosamente y tiene tamaño > 0.
    """
    binary_path, engine_type = find_headless_engine()
    if engine_type == "none":
        raise RuntimeError("No se encontró ningún motor PDF (Chromium, Brave, Chrome o WeasyPrint).")

    temp_html = None
    if not is_file:
        fd, temp_html = tempfile.mkstemp(suffix=".html", prefix="docstudio_")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html_source)
        html_file = temp_html
    else:
        html_file = os.path.abspath(html_source)

    out_abs = os.path.abspath(output_pdf_path)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)

    success = False
    try:
        if engine_type == "chromium":
            cmd = [
                binary_path,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--run-all-compositor-stages-before-draw",
                "--no-pdf-header-footer",
                f"--print-to-pdf={out_abs}",
                html_file
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            success = os.path.exists(out_abs) and os.path.getsize(out_abs) > 0
        elif engine_type == "weasyprint":
            if binary_path == "python_module":
                from weasyprint import HTML
                HTML(filename=html_file).write_pdf(out_abs)
                success = True
            else:
                cmd = [binary_path, html_file, out_abs]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                success = res.returncode == 0 and os.path.exists(out_abs)
    finally:
        if temp_html and os.path.exists(temp_html):
            try:
                os.remove(temp_html)
            except Exception:
                pass

    return success

