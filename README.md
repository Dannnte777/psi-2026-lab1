# PSI 2-2026 - Laboratorio 1: del muestreo al filtrado

![CI](https://github.com/gustav0vasq/psi-2026-lab1/actions/workflows/ci.yml/badge.svg)

## Instalación y uso sin Docker
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,caso]"
pytest -v
psi-lab1            # regenera figuras y tablas en out/
```

## Uso con Docker
```bash
docker compose build
docker compose run --rm tests   # pruebas unitarias y de integracion
docker compose run --rm lab1    # reproduce todas las figuras y tablas en out/
```

## Datos
No se versionan. `datos.py` los descarga o genera (carpeta `data/`, o `PSI_DATOS`).
El CI usa solo señales sintéticas (`psi-lab1 --sintetico`).

## Interfaz pública (módulo, firma, unidades, forma)
| Módulo | Función | Argumentos | Retorna |
|---|---|---|---|
| `psi_lab.lab1.muestreo` | `muestrear(fun, fs, duracion)` | fun: callable de t [s]; fs [Hz]; duracion [s] | `(t, x)` arreglos 1D de largo `round(fs*duracion)` |
| `psi_lab.lab1.sinteticos` | `tono(f, fs, duracion)` | f [Hz]; fs [Hz]; duracion [s] | `x` 1D de largo `round(fs*duracion)`, `cos(2 pi f t)` de amplitud 1 |
| `psi_lab.lab1.sinteticos` | `suma_tonos(frecuencias, fs, duracion)` | frecuencias: secuencia de f [Hz]; fs [Hz]; duracion [s] | `x` 1D, suma de tonos de amplitud 1 |
| `psi_lab.lab1.sinteticos` | `chirp(f0, f1, fs, duracion)` | f0, f1 [Hz]; fs [Hz]; duracion [s] | `x` 1D, barrido lineal de f0 a f1, amplitud 1 |
| `psi_lab.lab1.sinteticos` | `ruido_a_snr(x, snr_db, semilla=0)` | x: arreglo 1D; snr_db [dB]; semilla: entero | `x + ruido` blanco gaussiano con SNR exacto `10 log10(P_x / P_ruido) = snr_db`; reproducible por semilla |
| ... | ... | ... | ... |


## Estructura
`src/psi_lab/lab1/` (código), `tests/lab1/{unit,integration}/`, `informe/lab1.pdf`.