"""Utilidades del taller: datos y transformaciones del marketing mix model.

Replican la metodología de Google Meridian (Apache-2.0) para un modelo nacional:
escalado del KPI y de los medios, adstock geométrico normalizado y saturación de
Hill. El modelo de pymc no está aquí: se escribe en el notebook, porque *es* el
contenido del taller.

Uso:

    from src.mmm import CANALES, cargar_datos, matriz_rezagos
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Los cinco canales de pago del fichero de Meridian.
CANALES = [f"Channel{i}" for i in range(5)]

# Controles del fichero. El canal orgánico y `Promo` se quedan fuera del taller.
CONTROLES = ["competitor_sales_control", "sentiment_score_control"]

# Rezagos máximos del adstock. Es el valor por defecto de Meridian (DEFAULT_MAX_LAG).
MAX_LAG = 8


def cargar_datos(raiz: Path | str = ".") -> pd.DataFrame:
    """Carga el fichero de Meridian y añade la columna `revenue`.

    El KPI del taller son los ingresos: conversiones por ingreso medio de cada
    conversión. Así el ROI queda en euros por euro y la priori por defecto de
    Meridian sobre el ROI se puede usar tal cual.
    """
    df = pd.read_csv(Path(raiz) / "data" / "meridian_national.csv", parse_dates=["time"])
    df["revenue"] = df["conversions"] * df["revenue_per_conversion"]
    return df


def escalar_kpi(y: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Centra y escala el KPI. Devuelve la serie escalada, su media y su sd.

    Es el `KpiTransformer` de Meridian con población igual a 1, que es lo que
    corresponde a un modelo nacional.
    """
    media, sd = y.mean(), y.std()
    return (y - media) / sd, media, sd


def escalar_medios(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Divide cada canal por la mediana de sus valores positivos.

    Es el `MediaTransformer` de Meridian. La mediana se calcula ignorando los
    ceros: una semana sin inversión no dice nada sobre la escala del canal.
    """
    escala = np.array([np.median(col[col > 0]) for col in x.T])
    return x / escala, escala


def escalar_controles(z: np.ndarray) -> np.ndarray:
    """Deja cada control con media cero y desviación típica uno."""
    return (z - z.mean(axis=0)) / z.std(axis=0)


def matriz_rezagos(x: np.ndarray, max_lag: int = MAX_LAG) -> np.ndarray:
    """Apila los rezagos de cada canal en un array `(T, max_lag + 1, M)`.

    La posición `[t, l, m]` guarda el valor del canal `m` en `t - l`, con ceros
    antes del principio de la serie. Con esto el adstock es un producto de
    matrices y no hace falta ningún bucle dentro del modelo.
    """
    n_periodos, n_canales = x.shape
    rezagos = np.zeros((n_periodos, max_lag + 1, n_canales))
    for lag in range(max_lag + 1):
        rezagos[lag:, lag, :] = x[: n_periodos - lag, :]
    return rezagos


def pesos_adstock(alpha, max_lag: int = MAX_LAG):
    """Pesos del adstock geométrico, normalizados para que sumen uno.

    `w_l = alpha^l / sum_l alpha^l`. Al normalizar, el adstock es una media
    ponderada del pasado reciente y no una suma: cambiar `alpha` reparte la
    inversión en el tiempo, pero no infla su efecto total.

    Funciona con arrays de numpy y con variables de pytensor, así que la misma
    función sirve para los gráficos y para el modelo.
    """
    lags = np.arange(max_lag + 1)
    pesos = alpha[:, None] ** lags[None, :]
    return pesos / pesos.sum(axis=1, keepdims=True)


def hill(x, ec, slope=1.0):
    """Saturación de Hill: `x^slope / (x^slope + ec^slope)`.

    Va de 0 a 1 y vale 0.5 cuando `x == ec`: `ec` es el punto de media
    saturación, medido en medianas del canal.
    """
    return x**slope / (x**slope + ec**slope)


def vida_media(alpha: float) -> float:
    """Semanas hasta que el efecto de una impresión cae a la mitad."""
    return np.log(0.5) / np.log(alpha)
