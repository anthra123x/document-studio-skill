# -*- coding: utf-8 -*-
"""
Builder de documentos PDF con API fluida y estructurada.
Elimina la necesidad de escribir scripts auxiliares desechables o maquetar HTML crudo.
"""

import os
from typing import List, Dict, Optional, Union
from .compiler import compile_pdf

THEMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "themes"))

class Document:
    def __init__(
        self,
        title: str = "Documento",
        category: str = "DOCUMENTO TÉCNICO",
        theme: str = "modern",
        size: str = "letter",
        running_title: Optional[str] = None,
        footer_note: str = "Confidencial / Uso Interno"
    ):
        self.title = title
        self.category = category
        self.theme = theme.lower()
        self.size = size.lower()
        self.running_title = running_title or title
        self.footer_note = footer_note
        self.elements: List[str] = []
        self._cover_html: Optional[str] = None

    def set_cover(
        self,
        title: str,
        subtitle: Optional[str] = None,
        author: Optional[str] = None,
        organization: Optional[str] = None,
        date: Optional[str] = None,
        category: Optional[str] = None
    ) -> "Document":
        """Agrega una cabecera de portada compacta y profesional."""
        cat_text = category or self.category
        sub_html = f'<div class="cover-lead">{subtitle}</div>' if subtitle else ""
        meta_items = []
        if author:
            meta_items.append(f"<strong>Autor:</strong> {author}")
        if organization:
            meta_items.append(f"<strong>Organización:</strong> {organization}")
        if date:
            meta_items.append(f"<strong>Fecha:</strong> {date}")

        meta_html = " · ".join(meta_items)

        self._cover_html = f"""
        <div class="cover-compact">
            <div class="cover-category">{cat_text}</div>
            <h1 class="cover-main-title" style="border:none; margin:0 0 6px 0; padding:0;">{title}</h1>
            {sub_html}
            <div class="cover-meta">{meta_html}</div>
        </div>
        """
        return self

    def add_section(self, title: str) -> "Document":
        """Agrega un encabezado de sección principal (H1) que nunca queda huérfano."""
        self.elements.append(f"<h1>{title}</h1>")
        return self

    def add_subsection(self, title: str) -> "Document":
        """Agrega un subtítulo H2."""
        self.elements.append(f"<h2>{title}</h2>")
        return self

    def add_paragraph(self, text: str) -> "Document":
        """Agrega un párrafo justificado."""
        self.elements.append(f"<p>{text}</p>")
        return self

    def add_card(self, title: str, content: str) -> "Document":
        """Agrega una tarjeta atómica de contenido que no se fragmenta en salto de página."""
        self.elements.append(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div>{content}</div>
        </div>
        """)
        return self

    def add_kpis(self, kpi_list: List[Dict[str, str]]) -> "Document":
        """
        Agrega una fila de métricas/KPIs destacados en 2, 3 o 4 columnas.
        Ejemplo: [{'value': '99.9%', 'label': 'Uptime'}, {'value': '12ms', 'label': 'Latencia'}]
        """
        count = len(kpi_list)
        grid_class = f"grid-{min(max(count, 2), 4)}"
        cols_html = []
        for item in kpi_list:
            cols_html.append(f"""
            <div class="col">
                <div class="kpi-box">
                    <div class="kpi-value">{item.get('value', '')}</div>
                    <div class="kpi-label">{item.get('label', '')}</div>
                </div>
            </div>
            """)
        self.elements.append(f'<div class="{grid_class}">{"".join(cols_html)}</div>')
        return self

    def add_columns(self, column_html_list: List[str]) -> "Document":
        """Distribuye fragmentos HTML en 2, 3 o 4 columnas equilibradas."""
        count = len(column_html_list)
        grid_class = f"grid-{min(max(count, 2), 4)}"
        cols_html = "".join([f'<div class="col">{html}</div>' for html in column_html_list])
        self.elements.append(f'<div class="{grid_class}">{cols_html}</div>')
        return self

    def add_callout(self, title: str, text: str, kind: str = "info") -> "Document":
        """
        Agrega un cuadro destacado semántico.
        kind: 'info', 'success', 'warning', 'danger'.
        """
        kind_class = f"callout-{kind}"
        self.elements.append(f"""
        <div class="callout {kind_class}">
            <strong>{title}:</strong> {text}
        </div>
        """)
        return self

    def add_table(self, headers: List[str], rows: List[List[Union[str, int, float]]]) -> "Document":
        """Agrega una tabla de datos compacta con estilos editoriales limpios."""
        th_html = "".join([f"<th>{h}</th>" for h in headers])
        tr_html = []
        for row in rows:
            tds = "".join([f"<td>{cell}</td>" for cell in row])
            tr_html.append(f"<tr>{tds}</tr>")
        
        self.elements.append(f"""
        <table class="data-table">
            <thead><tr>{th_html}</tr></thead>
            <tbody>{"".join(tr_html)}</tbody>
        </table>
        """)
        return self

    def add_code(self, code_str: str, language: str = "") -> "Document":
        """Agrega un bloque de código formateado monoespaciado."""
        clean_code = code_str.strip().replace("<", "&lt;").replace(">", "&gt;")
        self.elements.append(f"<pre><code>{clean_code}</code></pre>")
        return self

    def add_raw_html(self, html: str) -> "Document":
        """Permite inyectar cualquier fragmento HTML personalizado."""
        self.elements.append(html)
        return self

    def build_html(self) -> str:
        """Ensambla el documento completo con CSS base y tema seleccionado."""
        # Cargar CSS base
        base_css_file = os.path.join(THEMES_DIR, "base.css")
        with open(base_css_file, "r", encoding="utf-8") as f:
            css = f.read()

        # Cargar CSS del tema si existe
        theme_css_file = os.path.join(THEMES_DIR, f"{self.theme}.css")
        if os.path.exists(theme_css_file):
            with open(theme_css_file, "r", encoding="utf-8") as f:
                css += "\n" + f.read()

        body_content = ""
        if self._cover_html:
            body_content += self._cover_html
        body_content += "\n".join(self.elements)

        full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        :root {{
            --doc-running-title: "{self.running_title}";
            --doc-category: "{self.category}";
            --doc-footer-note: "{self.footer_note}";
        }}
        {css}
    </style>
</head>
<body>
    {body_content}
</body>
</html>
"""
        return full_html

    def render(self, output_pdf_path: str) -> bool:
        """Compila y exporta directamente el documento a PDF en la ruta indicada."""
        html = self.build_html()
        return compile_pdf(html, output_pdf_path, is_file=False, page_size=self.size)
