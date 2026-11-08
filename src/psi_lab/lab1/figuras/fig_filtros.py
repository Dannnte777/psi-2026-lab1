"""Figuras y tabla de la Tarea 4 (filtros FIR por ventana). Dueno: R3."""

import numpy as np
from matplotlib.figure import Figure

from psi_lab.lab1.figuras import figura, guardar_tabla
from psi_lab.lab1.filtros import (
    VENTANAS,
    filtrar,
    fir_pasaaltos,
    fir_pasabajos,
    fir_pasabanda,
    fir_rechazabanda,
    medir_pasabajos,
    respuesta_frecuencia,
)
from psi_lab.lab1.sinteticos import ruido_a_snr, suma_tonos, tono

FS = 1000.0  # [Hz]
FC = 100.0  # corte del pasabajos de referencia [Hz]
N_COEF = 101
N_COEFS_TABLA = (25, 51, 101, 201)


def _db(H):
    return 20 * np.log10(np.maximum(np.abs(H), 1e-8))


@figura("filtros_tipos")
def _(salida):
    filtros = {
        f"pasabajos fc={FC:g} Hz": fir_pasabajos(FC, FS, N_COEF),
        f"pasaaltos fc={FC:g} Hz": fir_pasaaltos(FC, FS, N_COEF),
        "pasabanda 150-250 Hz": fir_pasabanda(150, 250, FS, N_COEF),
        "rechazabanda 150-250 Hz": fir_rechazabanda(150, 250, FS, N_COEF),
    }
    fig = Figure(figsize=(9, 6))
    axs = fig.subplots(2, 2, sharex=True, sharey=True).ravel()
    for ax, (nombre, h) in zip(axs, filtros.items()):
        freqs, H = respuesta_frecuencia(h, FS)
        ax.plot(freqs, _db(H), lw=0.9)
        ax.set(title=nombre, ylim=(-100, 5))
        ax.grid(alpha=0.3)
    for ax in axs[2:]:
        ax.set_xlabel("f [Hz]")
    for ax in axs[::2]:
        ax.set_ylabel("|H(f)| [dB]")
    fig.suptitle(f"Filtros derivados del pasabajos (Hamming, n_coef={N_COEF}, fs={FS:g} Hz)")
    fig.tight_layout()
    fig.savefig(salida / "filtros_tipos.png", dpi=120)


@figura("filtros_ventanas")
def _(salida):
    fig = Figure(figsize=(9, 4))
    ax_h, ax_f = fig.subplots(1, 2, gridspec_kw={"width_ratios": [1, 2]})
    for v in VENTANAS:
        h = fir_pasabajos(FC, FS, N_COEF, v)
        freqs, H = respuesta_frecuencia(h, FS)
        ax_h.plot(np.arange(N_COEF) - N_COEF // 2, h, lw=0.9, label=v)
        ax_f.plot(freqs, _db(H), lw=0.9, label=v)
    ax_h.set(xlabel="n - M", ylabel="h[n]", title="Respuesta al impulso")
    ax_f.set(xlabel="f [Hz]", ylabel="|H(f)| [dB]", ylim=(-120, 5),
             title=f"Pasabajos fc={FC:g} Hz, n_coef={N_COEF}")
    ax_f.legend()
    for ax in (ax_h, ax_f):
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(salida / "filtros_ventanas.png", dpi=120)


@figura("filtros_n_coef")
def _(salida):
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    for n in N_COEFS_TABLA:
        freqs, H = respuesta_frecuencia(fir_pasabajos(FC, FS, n), FS)
        ax.plot(freqs, np.abs(H), lw=0.9, label=f"n_coef={n}")
    ax.axvline(FC, color="k", ls=":", lw=0.8)
    ax.set(xlabel="f [Hz]", ylabel="|H(f)|", xlim=(0, 250),
           title="Hamming: mas coeficientes, transicion mas angosta (misma atenuacion)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(salida / "filtros_n_coef.png", dpi=120)

    filas = []
    for v in VENTANAS:
        for n in N_COEFS_TABLA:
            ancho, aten = medir_pasabajos(fir_pasabajos(FC, FS, n, v), FS, FC)
            filas.append([v, n, f"{ancho:.2f}", f"{ancho * n / FS:.2f}", f"{aten:.1f}"])
    guardar_tabla(
        salida,
        "filtros_transicion_atenuacion",
        ["ventana", "n_coef", "ancho_transicion_hz", "ancho_por_n_sobre_fs", "atenuacion_db"],
        filas,
    )


@figura("filtros_aplicacion")
def _(salida):
    duracion = 0.4
    t = np.arange(round(FS * duracion)) / FS
    limpia = tono(50, FS, duracion)
    x = ruido_a_snr(suma_tonos([50, 300], FS, duracion), snr_db=5, semilla=0)
    salidas = {
        "pasabajos 100 Hz": filtrar(x, fir_pasabajos(FC, FS, N_COEF)),
        "rechazabanda 250-350 Hz": filtrar(x, fir_rechazabanda(250, 350, FS, N_COEF)),
    }
    fig = Figure(figsize=(9, 5))
    axs = fig.subplots(3, 1, sharex=True)
    axs[0].plot(t, x, lw=0.7)
    axs[0].set(ylabel="x", title="Entrada: tonos de 50 y 300 Hz + ruido blanco (SNR 5 dB)")
    for ax, (nombre, y) in zip(axs[1:], salidas.items()):
        ax.plot(t, limpia, "k--", lw=0.8, label="tono de 50 Hz")
        ax.plot(t, y, lw=0.9, label=nombre)
        ax.axvspan(0, N_COEF // 2 / FS, color="0.9")
        ax.axvspan(duracion - N_COEF // 2 / FS, duracion, color="0.9")
        ax.set(ylabel="y")
        ax.legend(loc="upper right", fontsize=8)
    axs[-1].set_xlabel("t [s]  (gris: transitorio de los bordes)")
    fig.tight_layout()
    fig.savefig(salida / "filtros_aplicacion.png", dpi=120)
