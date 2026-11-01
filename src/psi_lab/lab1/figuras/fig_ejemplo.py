"""Figura de relleno para probar la tuberia. Se elimina cuando haya figuras reales."""

import numpy as np
from matplotlib.figure import Figure

from psi_lab.lab1.figuras import figura
from psi_lab.lab1.muestreo import muestrear


@figura("ejemplo")
def _(salida):
    t, x = muestrear(lambda t: np.sin(2 * np.pi * 5 * t), fs=100, duracion=1)
    fig = Figure(figsize=(6, 3))
    ax = fig.subplots()
    ax.plot(t, x, ".-")
    ax.set(xlabel="t [s]", ylabel="x(t)", title="Figura de ejemplo")
    fig.tight_layout()
    fig.savefig(salida / "ejemplo.png", dpi=120)
