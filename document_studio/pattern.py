# -*- coding: utf-8 -*-
"""
Motor de Patrones de Diseño (Design Pattern Engine) de Document Studio.
Permite al usuario definir el patrón visual (colores, fuentes, geometría, componentes)
y la skill se encarga de aplicarlo automáticamente a documentos PDF y presentaciones PPTX.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union

@dataclass
class DesignPattern:
    """
    Especificación de un patrón de diseño editorial.
    """
    name: str = "Personalizado"
    primary_color: str = "#0F172A"       # Color dominante / acento principal
    secondary_color: str = "#334155"     # Color secundario
    accent_color: str = "#38BDF8"        # Color de resalte / badges / alertas
    bg_color: str = "#FFFFFF"            # Fondo del documento
    card_bg: str = "#F8FAFC"             # Fondo de tarjetas y KPIs
    text_color: str = "#1E293B"          # Color del texto base
    border_color: str = "#E2E8F0"        # Bordes de tablas y separadores
    font_heading: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_body: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    page_size: str = "letter"            # 'letter' o 'a4'
    page_margin: str = "14mm"            # Margen de página
    show_running_headers: bool = True     # Encabezados en cada página
    show_page_numbers: bool = True       # Paginación 'Página X de Y'
    footer_note: str = ""                # Nota de confidencialidad o pie
    custom_css: str = ""                 # Reglas CSS específicas adicionales
    extra_tokens: Dict[str, Any] = field(default_factory=dict)

    def to_css(self) -> str:
        """Genera el bloque CSS de variables y reglas basado en el patrón."""
        return f"""
        :root {{
            --primary-color: {self.primary_color};
            --secondary-color: {self.secondary_color};
            --accent-color: {self.accent_color};
            --bg-color: {self.bg_color};
            --card-bg: {self.card_bg};
            --text-color: {self.text_color};
            --heading-color: {self.primary_color};
            --border-color: {self.border_color};
            --table-header-bg: {self.primary_color};
            --table-zebra: {self.card_bg};
        }}
        body {{
            font-family: {self.font_body};
            color: {self.text_color};
            background-color: {self.bg_color};
        }}
        h1, h2, h3, h4, th, .card-title, .kpi-label {{
            font-family: {self.font_heading};
        }}
        h1 {{
            border-bottom: 2px solid {self.primary_color};
        }}
        @page {{
            size: {self.page_size};
            margin: {self.page_margin};
        }}
        {self.custom_css}
        """

    @classmethod
    def from_name(cls, name: str) -> "DesignPattern":
        """Retorna un patrón preconfigurado a partir de su identificador."""
        name_clean = name.lower().strip()
        presets = {
            "executive": cls(
                name="Executive Corporate",
                primary_color="#1E3A8A", # Deep Navy
                secondary_color="#0F172A",
                accent_color="#D97706",  # Gold
                card_bg="#F8FAFC",
                text_color="#1E293B",
                border_color="#CBD5E1"
            ),
            "modern": cls(
                name="Modern Tech",
                primary_color="#4F46E5", # Indigo
                secondary_color="#1E1B4B",
                accent_color="#06B6D4",  # Cyan
                card_bg="#F9FAFB",
                text_color="#374151",
                border_color="#E5E7EB"
            ),
            "academic_ufps": cls(
                name="Académico UFPS Seccional Ocaña",
                primary_color="#C8102E", # Rojo UFPS
                secondary_color="#0F172A",
                accent_color="#38BDF8",  # Tiza cian
                card_bg="#F8FAFC",
                text_color="#1E293B",
                border_color="#CBD5E1",
                footer_note="UFPS Seccional Ocaña · Ingeniería de Sistemas"
            ),
            "minimal": cls(
                name="Minimal Swiss",
                primary_color="#000000",
                secondary_color="#171717",
                accent_color="#525252",
                card_bg="#FFFFFF",
                text_color="#171717",
                border_color="#000000",
                font_heading="-apple-system, 'Helvetica Neue', Arial, sans-serif",
                font_body="-apple-system, 'Helvetica Neue', Arial, sans-serif"
            ),
            "dark": cls(
                name="Cyber Dark Terminal",
                primary_color="#38BDF8",
                secondary_color="#818CF8",
                accent_color="#4ADE80",
                bg_color="#0F172A",
                card_bg="#1E293B",
                text_color="#F8FAFC",
                border_color="#334155",
                custom_css="""
                body { background-color: #0F172A !important; color: #F8FAFC !important; }
                h1, h2, h3 { color: #F8FAFC !important; }
                p, li { color: #CBD5E1 !important; }
                table.data-table th { background-color: #1E293B !important; color: #38BDF8 !important; }
                table.data-table td { color: #E2E8F0 !important; }
                table.data-table tr:nth-child(even) { background-color: #162032 !important; }
                """
            )
        }
        return presets.get(name_clean, presets["modern"])

    @classmethod
    def resolve(cls, pattern_input: Union[str, "DesignPattern", Dict[str, Any]]) -> "DesignPattern":
        """Resuelve dinámicamente cualquier entrada (nombre, dict o instancia) a un DesignPattern."""
        if isinstance(pattern_input, DesignPattern):
            return pattern_input
        if isinstance(pattern_input, dict):
            return cls(**pattern_input)
        if isinstance(pattern_input, str):
            return cls.from_name(pattern_input)
        return cls.from_name("modern")
