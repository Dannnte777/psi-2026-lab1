"""Caso C, tarea C2: interferencia periodica sintetica y deteccion de sus picos."""


def coseno_2d(forma, ku, kv, amplitud):
    """Coseno amplitud * cos(2 pi (ku x / ancho + kv y / alto)), con forma = (alto, ancho).

    ku y kv son ciclos ENTEROS sobre la imagen completa: los picos caen exactamente en los
    bins (kv, ku) y (alto - kv, ancho - ku) del espectro sin shift.
    """
    raise NotImplementedError


def agregar_interferencia(img, ku, kv, amplitud):
    """Suma coseno_2d(img.shape, ku, kv, amplitud) a img (sin recortar a [0, 1])."""
    raise NotImplementedError


def detectar_picos(E, umbral):
    """Picos de |E| por sobre `umbral` (fraccion del maximo de |E| fuera del DC).

    Excluye el DC (bin [0, 0]) y devuelve SIEMPRE ambos picos de cada par conjugado.
    Retorna un arreglo (n_picos, 2) de enteros, columnas (v, u) = (fila, columna).
    """
    raise NotImplementedError
