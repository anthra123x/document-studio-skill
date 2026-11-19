# -*- coding: utf-8 -*-
"""
Generador de diagramas técnicos vectoriales de ingeniería en alta resolución.
Elimina por completo las ilustraciones alucinadas («AI-slop»).
"""

import os
import shutil
import tempfile
import subprocess
from typing import List, Dict

def find_browser():
    for candidate in ["brave", "brave-browser", "chromium", "chromium-browser", "google-chrome"]:
        p = shutil.which(candidate)
        if p:
            return p
    return None

class Diagram:
    @staticmethod
    def render_html(html_body: str, output_png_path: str, width: int = 1200, height: int = 900) -> bool:
        """Renderiza cualquier fragmento HTML5/CSS Grid a una imagen PNG de 1200x900 (4:3) o 1920x1080 (16:9)."""
        browser = find_browser()
        if not browser:
            return False

        full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        width: {width}px;
        height: {height}px;
        background-color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }}
    .diagram-container {{
        width: 100%;
        height: 100%;
        padding: 36px 44px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
</style>
</head>
<body>
    <div class="diagram-container">
        {html_body}
    </div>
</body>
</html>
"""
        out_abs = os.path.abspath(output_png_path)
        os.makedirs(os.path.dirname(out_abs), exist_ok=True)

        fd, temp_file = tempfile.mkstemp(suffix=".html", prefix="diagram_")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(full_html)

        try:
            cmd = [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--window-size={width},{height}",
                f"--screenshot={out_abs}",
                temp_file
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return os.path.exists(out_abs) and os.path.getsize(out_abs) > 0

    @classmethod
    def flow(cls, title: str, steps: List[Dict[str, str]], output_png: str, width: int = 1200, height: int = 900) -> bool:
        """Genera un diagrama de flujo horizontal moderno."""
        cols = len(steps)
        step_boxes = []
        for i, s in enumerate(steps):
            accent = s.get("color", "#38BDF8")
            step_boxes.append(f"""
            <div style="background-color: #1E293B; border: 1.5px solid {accent}; border-radius: 8px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 11px; font-weight: 800; color: {accent}; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px;">FASE {i+1}</div>
                    <div style="font-size: 18px; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">{s.get('title', '')}</div>
                    <p style="font-size: 13px; color: #94A3B8; line-height: 1.45;">{s.get('desc', '')}</p>
                </div>
            </div>
            """)

        html = f"""
        <div style="border-bottom: 2px solid #38BDF8; padding-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.2px;">{title}</span>
            <span style="background-color: #1E293B; border: 1px solid #334155; color: #38BDF8; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 700;">ARQUITECTURA DE FLUJO</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat({cols}, 1fr); gap: 20px; margin: 30px 0; flex-grow: 1;">
            {"".join(step_boxes)}
        </div>
        <div style="background-color: #0B1120; border: 1px solid #1E293B; border-radius: 6px; padding: 12px 18px; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #64748B; font-size: 12px;">ESTÁNDAR EDITORIAL DE INGENIERÍA · DOCUMENT STUDIO</span>
            <span style="color: #38BDF8; font-size: 12px; font-weight: 600;">ALTA DISPONIBILIDAD & RENDIMIENTO</span>
        </div>
        """
        return cls.render_html(html, output_png, width=width, height=height)
