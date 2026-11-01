"""Caso C, tarea C1: DFT 2D. El arreglo de trabajo va SIN fftshift (DC en E[0, 0])."""


def dft2(img):
    """DFT 2D como DFT 1D por filas y luego por columnas. Retorna E complejo, forma de img."""
    raise NotImplementedError


def idft2(E):
    """DFT 2D inversa. Retorna un arreglo complejo; la imagen es `.real`."""
    raise NotImplementedError


def espectro_log(E):
    """Magnitud en escala log, YA centrada (fftshift). Solo para graficar."""
    raise NotImplementedError


def fase(E):
    """Fase de E en radianes, en [-pi, pi]. Misma forma que E, sin shift."""
    raise NotImplementedError
