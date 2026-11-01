import numpy as np
import pytest

from psi_lab.lab1.sinteticos import chirp, ruido_a_snr, suma_tonos, tono

FS = 1000


def _pico(x, fs=FS):
    return np.fft.rfftfreq(x.size, 1 / fs)[np.argmax(np.abs(np.fft.rfft(x)))]


def test_tono_pico_en_su_frecuencia():
    assert _pico(tono(50, FS, 1)) == pytest.approx(50)


def test_tono_largo_amplitud_y_fase():
    x = tono(10, FS, 2)
    assert x.size == 2 * FS
    assert x[0] == pytest.approx(1)
    assert np.max(np.abs(x)) <= 1 + 1e-12


def test_suma_tonos_es_la_suma_de_tonos():
    frecs = [50, 120, 300]
    esperado = sum(tono(f, FS, 1) for f in frecs)
    assert np.allclose(suma_tonos(frecs, FS, 1), esperado)


def test_suma_tonos_tiene_un_pico_por_frecuencia():
    amp = np.abs(np.fft.rfft(suma_tonos([50, 120], FS, 1)))
    assert set(np.argsort(amp)[-2:]) == {50, 120}


def test_chirp_parte_y_termina_en_sus_frecuencias():
    # En un tramo corto la frecuencia es casi constante: la del centro del tramo.
    duracion, tramo = 10, 0.5
    x = chirp(50, 400, FS, duracion)
    n = round(tramo * FS)
    tol = 350 * tramo / duracion  # barrido dentro del tramo (17.5 Hz)
    assert _pico(x[:n]) == pytest.approx(50 + 350 * tramo / 2 / duracion, abs=tol)
    assert _pico(x[-n:]) == pytest.approx(400 - 350 * tramo / 2 / duracion, abs=tol)


def test_chirp_con_f0_igual_f1_es_un_tono():
    assert np.allclose(chirp(80, 80, FS, 1), tono(80, FS, 1))


@pytest.mark.parametrize("snr_db", [-5, 0, 10, 30])
def test_ruido_a_snr_es_exacto(snr_db):
    x = tono(50, FS, 1)
    ruido = ruido_a_snr(x, snr_db) - x
    snr = 10 * np.log10(np.mean(x**2) / np.mean(ruido**2))
    assert snr == pytest.approx(snr_db)


def test_ruido_a_snr_reproducible_segun_semilla():
    x = tono(50, FS, 1)
    assert np.array_equal(ruido_a_snr(x, 5, semilla=3), ruido_a_snr(x, 5, semilla=3))
    assert not np.allclose(ruido_a_snr(x, 5, semilla=3), ruido_a_snr(x, 5, semilla=4))


def test_ruido_a_snr_no_modifica_la_entrada():
    x = tono(50, FS, 1)
    copia = x.copy()
    ruido_a_snr(x, 0)
    assert np.array_equal(x, copia)


def test_ruido_a_snr_senal_nula_falla():
    with pytest.raises(ValueError):
        ruido_a_snr(np.zeros(10), 0)
