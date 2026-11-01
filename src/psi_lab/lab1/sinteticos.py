"""Senales 1D de prueba compartidas por la parte comun y sus pruebas."""

import numpy as np

from psi_lab.lab1.muestreo import muestrear


def tono(f, fs, duracion):
    """Senoidal cos(2 pi f t) de amplitud 1 muestreada a fs Hz. Retorna x."""
    return muestrear(lambda t: np.cos(2 * np.pi * f * t), fs, duracion)[1]


def suma_tonos(frecuencias, fs, duracion):
    """Suma de senoidales de amplitud 1, una por cada frecuencia (Hz). Retorna x."""
    return muestrear(
        lambda t: sum(np.cos(2 * np.pi * f * t) for f in frecuencias), fs, duracion
    )[1]


def chirp(f0, f1, fs, duracion):
    """Barrido lineal de f0 a f1 Hz en `duracion` s, de amplitud 1. Retorna x.

    La frecuencia instantanea es f(t) = f0 + (f1 - f0) t / duracion, asi que la fase es
    2 pi (f0 t + (f1 - f0) t^2 / (2 duracion)).
    """
    k = (f1 - f0) / duracion
    return muestrear(lambda t: np.cos(2 * np.pi * (f0 * t + k * t**2 / 2)), fs, duracion)[1]


def ruido_a_snr(x, snr_db, semilla=0):
    """Suma a x ruido blanco gaussiano con SNR = 10 log10(P_x / P_ruido) = snr_db.

    El ruido se escala con su potencia empirica, asi el SNR resultante es exacto y no solo
    esperado. Es reproducible para una misma semilla. Retorna x + ruido (x no se modifica).
    """
    x = np.asarray(x, dtype=float)
    p_senal = np.mean(x**2)
    if p_senal == 0:
        raise ValueError("x tiene potencia cero: el SNR no esta definido")
    ruido = np.random.default_rng(semilla).standard_normal(x.shape)
    ruido *= np.sqrt(p_senal / 10 ** (snr_db / 10) / np.mean(ruido**2))
    return x + ruido
