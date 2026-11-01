"""Caso C, tarea C3: filtros notch 2D. Las mascaras se aplican sobre el espectro SIN shift."""


def notch_ideal(forma, picos, radio):
    """Mascara H float en [0, 1] de forma `forma`: 0 a distancia <= radio de cada pico, 1 fuera.

    picos: (n_picos, 2) enteros (fila, columna), con ambos picos de cada par conjugado.
    """
    raise NotImplementedError


def notch_gaussiano(forma, picos, sigma):
    """Mascara H float en [0, 1]: 1 - suma de gaussianas de desviacion sigma [px] en cada pico."""
    raise NotImplementedError


def aplicar_mascara(img, H):
    """idft2(dft2(img) * H). Retorna complejo (la imagen filtrada es `.real`).

    Con un par conjugado completo en H la parte imaginaria es ~0.
    """
    raise NotImplementedError
