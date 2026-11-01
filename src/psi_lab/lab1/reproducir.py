"""Comando psi-lab1: regenera todas las figuras y tablas del informe."""
import argparse
from pathlib import Path

from psi_lab.lab1.figuras import generar


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="psi-lab1", description="Regenera las figuras y tablas del informe."
    )
    parser.add_argument("-o", "--salida", default="out", help="carpeta de salida")
    parser.add_argument(
        "--sintetico",
        action="store_true",
        help="usa solo senales sinteticas, sin descargar datos (CI)",
    )
    args = parser.parse_args(argv)

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    # Cada figura/tabla se registra desde su propio archivo en figuras/fig_*.py
    generar(salida, sintetico=args.sintetico)

    print("Resultados en", salida)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())