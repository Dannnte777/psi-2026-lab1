"""Caso C, tarea C5: aliasing espacial."""


def zone_plate(M):
    """Zone plate de M x M px: I(x, y) = (1 + cos(pi (x^2 + y^2) / M)) / 2, en [0, 1]."""
    raise NotImplementedError


def reducir(img, k):
    """Diezma tomando una de cada k muestras (img[::k, ::k]), sin filtrar antes."""
    raise NotImplementedError


def pasabajos_separable_2d(img, fc, n_coef):
    """Pasabajos 2D separable (filas y luego columnas) con fir_pasabajos(fc, 1, n_coef).

    fc en ciclos/pixel, en (0, 0.5]. Retorna una imagen de la misma forma que img.
    """
    raise NotImplementedError
