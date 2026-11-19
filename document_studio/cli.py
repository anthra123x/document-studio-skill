# -*- coding: utf-8 -*-
"""
Interfaz de Línea de Comandos (CLI) de Document Studio.
"""

import argparse
import sys
import os
from .pdf.compiler import compile_pdf
from .pdf.builder import Document

def main():
    parser = argparse.ArgumentParser(
        description="Document Studio: Generación rápida de documentos PDF y presentaciones con diseño editorial profesional."
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Comando: compile
    p_compile = subparsers.add_parser("compile", help="Compilar un archivo HTML existente a PDF")
    p_compile.add_argument("input_html", help="Ruta al archivo HTML de entrada")
    p_compile.add_argument("output_pdf", help="Ruta al archivo PDF de salida")
    p_compile.add_argument("--size", default="letter", choices=["letter", "a4"], help="Tamaño de papel")

    # Comando: quick-report
    p_quick = subparsers.add_parser("quick-report", help="Generar un informe ejecutivo rápido a partir de texto básico")
    p_quick.add_argument("--title", required=True, help="Título del informe")
    p_quick.add_argument("--output", required=True, help="Ruta del archivo PDF de salida")
    p_quick.add_argument("--theme", default="modern", choices=["executive", "modern", "academic", "minimal"], help="Tema cromático")
    p_quick.add_argument("--author", default="Equipo Técnico", help="Nombre del autor u organización")

    args = parser.parse_args()

    if args.command == "compile":
        success = compile_pdf(args.input_html, args.output_pdf, is_file=True, page_size=args.size)
        if success:
            sz = os.path.getsize(args.output_pdf) / 1024
            print(f"✓ PDF compilado exitosamente: {args.output_pdf} ({sz:.1f} KB)")
            sys.exit(0)
        else:
            print(f"✗ Falló la compilación de {args.output_pdf}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "quick-report":
        doc = Document(title=args.title, theme=args.theme)
        doc.set_cover(title=args.title, author=args.author)
        doc.add_section("1. Introducción y Contexto")
        doc.add_paragraph("Este documento fue generado automáticamente por Document Studio garantizando maquetación compacta y buenas prácticas de diseño editorial.")
        doc.add_card("Estado General", "<p>Todos los sistemas operativos y validados.</p>")
        success = doc.render(args.output)
        if success:
            sz = os.path.getsize(args.output) / 1024
            print(f"✓ Informe generado exitosamente: {args.output} ({sz:.1f} KB)")
            sys.exit(0)
        else:
            print(f"✗ Error al generar el informe", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
