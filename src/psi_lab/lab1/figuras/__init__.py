"""Registro de figuras del informe: cada figura vive en su propio archivo `fig_*.py`.

Un archivo nuevo solo tiene que decorar su funcion; `reproducir.py` no se modifica:

    @figura("notch_comparacion")
    def _(salida):
        ...
        fig.savefig(salida / "notch_comparacion.png", dpi=120)

`salida` es la carpeta de salida (Path). Las tablas se escriben con `guardar_tabla`.
Las figuras que necesitan datos reales se declaran con `requiere_datos=True` y se
omiten con `--sintetico`.
"""

import csv
import importlib
import pkgutil
from pathlib import Path

REGISTRO = {}


def figura(nombre, requiere_datos=False):
    """Decorador: registra `fun(salida)` como la figura `nombre`."""

    def registrar(fun):
        if nombre in REGISTRO:
            raise ValueError(f"figura duplicada: {nombre!r}")
        REGISTRO[nombre] = (fun, requiere_datos)
        return fun

    return registrar


def guardar_tabla(salida, nombre, encabezado, filas):
    """Escribe `salida/tablas/<nombre>.csv`. Retorna la ruta."""
    ruta = Path(salida) / "tablas" / f"{nombre}.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(encabezado)
        escritor.writerows(filas)
    return ruta


def descubrir():
    """Importa todos los modulos `fig_*` del paquete, lo que registra sus figuras."""
    for modulo in sorted(m.name for m in pkgutil.iter_modules(__path__)):
        if modulo.startswith("fig_"):
            importlib.import_module(f"{__name__}.{modulo}")


def generar(salida, sintetico=False):
    """Genera las figuras registradas en `salida`. Retorna los nombres generados."""
    descubrir()
    salida = Path(salida)
    generadas = []
    for nombre, (fun, requiere_datos) in sorted(REGISTRO.items()):
        if sintetico and requiere_datos:
            continue
        fun(salida)
        generadas.append(nombre)
    return generadas
