"""Issue #42: ¿el modelo de medios lleva saturación de Hill o no?

Script de trabajo, fuera de `_quarto.yml`. No es material de la charla: ajusta las dos
versiones del modelo de medios sobre los mismos datos y escupe por pantalla los números con
los que se toma la decisión. Se ejecuta a mano, una vez, y se conserva para que dentro de
seis meses la decisión se pueda reproducir en vez de recordarla.

    python scripts/comparar_hill.py

Tarda. Son hasta ocho ajustes de MCMC con los mismos `draws`, `tune` y `chains` que las
slides, porque el `target_accept` mínimo con el que cada versión muestrea limpio es
justamente uno de los números que hay que medir.
"""

import time

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
import pytensor.tensor as pt

SEMILLA = 42

CANALES = [f"Channel{i}" for i in range(5)]
CONTROLES = ["competitor_sales_control", "sentiment_score_control"]
MAX_LAG = 8  # rezagos del adstock, el valor por defecto de Meridian

# Los ajustes de las slides. No se bajan para que el script termine antes: el número que se
# busca es el `target_accept` mínimo con ESTE muestreo, no con uno más corto.
DRAWS, TUNE, CHAINS = 2000, 2000, 4
ESCALERA = [0.9, 0.95, 0.97, 0.99]

# Muestrea limpio = las tres cosas a la vez.
MAX_RHAT = 1.01
MIN_ESS = 400

# Fijado a la v1.1.5 a propósito: en `main`, un `git mv` de Google revienta el material.
URL_DATOS = (
    "https://raw.githubusercontent.com/google/meridian/v1.1.5/"
    "meridian/data/simulated_data/csv/national_all_channels.csv"
)
CSV_LOCAL = "data/meridian_national.csv"  # byte a byte el mismo fichero


def pesos_adstock(alpha, max_lag=MAX_LAG):
    # Vale para arrays de numpy y para variables de pytensor, así que la misma función
    # sirve para los dos modelos. Copiada de `notebooks/taller.ipynb`, celda-22.
    pesos = alpha[:, None] ** np.arange(max_lag + 1)[None, :]
    return pesos / pesos.sum(axis=1, keepdims=True)


def cargar_datos():
    try:
        df = pd.read_csv(URL_DATOS, parse_dates=["time"])
    except Exception as error:  # sin red, la copia offline
        print(f"! la URL ha fallado ({error}); leyendo {CSV_LOCAL}")
        df = pd.read_csv(CSV_LOCAL, parse_dates=["time"])
    df["revenue"] = df["conversions"] * df["revenue_per_conversion"]
    return df


def preparar(df):
    """El mismo escalado que el taller archivado y que pide el issue #43."""
    y = df["revenue"].to_numpy()
    y_media, y_sd = y.mean(), y.std()
    y_esc = (y - y_media) / y_sd

    z = df[CONTROLES].to_numpy()
    z_esc = (z - z.mean(axis=0)) / z.std(axis=0)

    # Cada canal, dividido por la mediana de sus semanas con inversión: una unidad es "una
    # semana normal de ese canal". Ni media ni máximo.
    x = df[[f"{c}_spend" for c in CANALES]].to_numpy()
    escala = np.array([np.median(col[col > 0]) for col in x.T])
    x_esc = x / escala

    # rezagos[t, l, m] = canal m en t - l, con ceros antes del principio de la serie.
    rezagos = np.zeros((len(df), MAX_LAG + 1, len(CANALES)))
    for lag in range(MAX_LAG + 1):
        rezagos[lag:, lag, :] = x_esc[: len(df) - lag, :]

    return dict(
        y=y,
        y_esc=y_esc,
        y_sd=y_sd,
        z_esc=z_esc,
        rezagos=rezagos,
        gasto_total=x.sum(axis=0),
        coords={"semana": df["time"].to_numpy(), "control": CONTROLES, "canal": CANALES},
    )


def construir(d, con_hill):
    """El modelo de medios, con y sin saturación.

    La única diferencia entre las dos versiones son las dos líneas de `ec` y la saturación.
    Todo lo demás —prioris, escalado, la derivación de `beta` desde el ROI— es idéntico, que
    es la condición para que la comparación signifique algo.
    """
    with pm.Model(coords=d["coords"]) as modelo:
        alpha = pm.Uniform("alpha", 0.0, 1.0, dims="canal")
        roi = pm.LogNormal("roi", mu=0.2, sigma=0.9, dims="canal")
        gamma = pm.Normal("gamma", 0.0, 1.0, dims="control")
        mu = pm.Normal("mu", 0.0, 5.0)  # ancha a propósito: compensa lo que aportan los medios
        sigma = pm.Exponential("sigma", 1.0)

        pesos = pesos_adstock(alpha)
        medios = pt.sum(d["rezagos"] * pesos.T[None, :, :], axis=1)  # (semanas, canales)

        if con_hill:
            # El defecto de Meridian (`meridian/model/prior_distribution.py`): `ec_m` es una
            # TruncatedNormal y `slope_m` es Deterministic(1.0). Con slope = 1, la curva de
            # Hill x**s / (x**s + ec**s) se queda en x / (x + ec). Va después del adstock,
            # como en `meridian/model/adstock_hill.py` para medios pagados.
            ec = pm.TruncatedNormal("ec", mu=0.8, sigma=0.8, lower=0.1, upper=10.0, dims="canal")
            medios = medios / (medios + ec)

        # Beta no es un parámetro libre: sale del ROI. Y se deduce sobre los medios tal como
        # entran en la media, saturados o no.
        beta = pm.Deterministic(
            "beta", roi * d["gasto_total"] / (d["y_sd"] * pt.sum(medios, axis=0)), dims="canal"
        )
        pm.Deterministic("contribucion", roi * d["gasto_total"], dims="canal")

        media = mu + pt.dot(medios, beta) + pt.dot(d["z_esc"], gamma)
        pm.Normal("y", mu=media, sigma=sigma, observed=d["y_esc"], dims="semana")

    return modelo


def simulacion_previa(modelo, d, etiqueta):
    with modelo:
        previa = pm.sample_prior_predictive(draws=2000, random_seed=SEMILLA)

    contribucion = previa.prior["contribucion"].values.reshape(-1, len(CANALES))
    pct = 100 * contribucion.sum(axis=1) / d["y"].sum()
    ingresos = previa.prior_predictive["y"].values.reshape(-1, len(d["y_esc"]))
    ingresos_eur = ingresos * d["y_sd"] + d["y"].mean()

    print(f"\n[{etiqueta}] simulación previa")
    print(f"  % de ingresos atribuido a medios: mediana {np.median(pct):5.1f} %"
          f" · p95 {np.percentile(pct, 95):6.1f} %")
    print(f"  ingresos semanales simulados: mediana {np.median(ingresos_eur) / 1e6:5.2f} M€"
          f" · observada {np.median(d['y']) / 1e6:.2f} M€")
    print(f"  semanas simuladas con ingresos negativos: {100 * (ingresos_eur < 0).mean():.1f} %")
    return dict(pct_mediana=np.median(pct), pct_p95=np.percentile(pct, 95))


def diagnostico(idata, variables):
    resumen = az.summary(idata, var_names=variables)
    return dict(
        divergencias=int(idata.sample_stats["diverging"].sum()),
        r_hat=float(resumen["r_hat"].max()),
        ess_bulk=int(resumen["ess_bulk"].min()),
    )


def ajustar(modelo, etiqueta, variables):
    """Sube la escalera de `target_accept` hasta que muestrea limpio."""
    print(f"\n[{etiqueta}] escalera de target_accept")
    for target in ESCALERA:
        with modelo:
            inicio = time.perf_counter()
            idata = pm.sample(
                draws=DRAWS, tune=TUNE, chains=CHAINS, target_accept=target,
                random_seed=SEMILLA, progressbar=False,
            )
            segundos = time.perf_counter() - inicio

        diag = diagnostico(idata, variables)
        limpio = (
            diag["divergencias"] == 0
            and diag["r_hat"] <= MAX_RHAT
            and diag["ess_bulk"] >= MIN_ESS
        )
        print(f"  target_accept={target:<5} divergencias={diag['divergencias']:<5}"
              f" r_hat={diag['r_hat']:.3f}  ess_bulk={diag['ess_bulk']:<6}"
              f" {segundos / 60:5.1f} min  {'limpio' if limpio else 'sucio'}")

        if limpio:
            return idata, dict(target_accept=target, segundos=segundos, **diag)

    print("  ! ninguno de la escalera muestrea limpio; me quedo con el último")
    return idata, dict(target_accept=ESCALERA[-1], segundos=segundos, **diag)


def tabla_roi(idata):
    roi = idata.posterior["roi"].values.reshape(-1, len(CANALES))
    hdi = az.hdi(idata, var_names=["roi"], hdi_prob=0.9)["roi"].values
    return pd.DataFrame({
        "roi_mediana": np.median(roi, axis=0),
        "hdi_bajo": hdi[:, 0],
        "hdi_alto": hdi[:, 1],
        "p_pierde_dinero": (roi < 1).mean(axis=0),
    }, index=CANALES)


def main():
    df = cargar_datos()
    d = preparar(df)
    print(f"{len(df)} semanas, de {df['time'].min():%Y-%m-%d} a {df['time'].max():%Y-%m-%d}")
    print(f"KPI estandarizado: media {d['y_esc'].mean():.3f}, sd {d['y_esc'].std():.3f}")
    print(f"huella de los datos escalados: y_esc {np.abs(d['y_esc']).sum():.6f}"
          f" · rezagos {d['rezagos'].sum():.6f}")

    resultados = {}
    for etiqueta, con_hill in [("sin Hill", False), ("con Hill", True)]:
        modelo = construir(d, con_hill=con_hill)
        variables = ["roi", "alpha", "gamma", "mu", "sigma"] + (["ec"] if con_hill else [])
        previa = simulacion_previa(modelo, d, etiqueta)
        idata, ajuste = ajustar(modelo, etiqueta, variables)
        resultados[etiqueta] = dict(idata=idata, previa=previa, ajuste=ajuste)

    sin_hill, con_hill = resultados["sin Hill"], resultados["con Hill"]

    print("\n" + "=" * 78)
    print("1. SIMULACIÓN PREVIA: ¿cambia lo que la priori considera posible?")
    print("=" * 78)
    print(pd.DataFrame({k: v["previa"] for k, v in resultados.items()}).round(2))
    print("\nOjo: `contribucion = roi · gasto` y la priori del ROI es la misma en las dos,")
    print("así que ese porcentaje es la MISMA DISTRIBUCIÓN en las dos versiones. La")
    print("reparametrización por ROI deja la contribución de medios a priori invariante a")
    print("Hill. Las décimas de diferencia son ruido de Monte Carlo: el modelo con Hill")
    print("tiene una variable más y el generador aleatorio no reparte igual.")

    print("\n" + "=" * 78)
    print("2 y 3. DIAGNÓSTICO Y TIEMPO")
    print("=" * 78)
    ajustes = pd.DataFrame({k: v["ajuste"] for k, v in resultados.items()}).T
    ajustes["minutos"] = (ajustes["segundos"] / 60).round(1)
    print(ajustes.drop(columns="segundos"))

    print("\n" + "=" * 78)
    print("4. LAS CONCLUSIONES: ¿cambia la frase final?")
    print("=" * 78)
    a, b = tabla_roi(sin_hill["idata"]), tabla_roi(con_hill["idata"])
    print("\nsin Hill:")
    print(a.round(2))
    print("\ncon Hill:")
    print(b.round(2))

    anchura = a["hdi_alto"] - a["hdi_bajo"]
    comparacion = pd.DataFrame({
        "anchura_sin": anchura,
        "anchura_con": b["hdi_alto"] - b["hdi_bajo"],
        "despl_bajo": (b["hdi_bajo"] - a["hdi_bajo"]) / anchura,
        "despl_alto": (b["hdi_alto"] - a["hdi_alto"]) / anchura,
        "despl_mediana": (b["roi_mediana"] - a["roi_mediana"]) / anchura,
    })
    print("\ndesplazamiento del HDI al 90 %, en anchuras del HDI sin Hill:")
    print(comparacion.round(2))
    print(f"\norden de canales por ROI mediano, sin Hill: "
          f"{list(a['roi_mediana'].sort_values(ascending=False).index)}")
    print(f"orden de canales por ROI mediano, con Hill: "
          f"{list(b['roi_mediana'].sort_values(ascending=False).index)}")

    print("\nCriterio 1: ¿dicen los datos algo sobre `ec`, o devuelve la priori?")
    ec_post = con_hill["idata"].posterior["ec"].values.reshape(-1, len(CANALES))
    ec_previa = pm.draw(
        pm.TruncatedNormal.dist(mu=0.8, sigma=0.8, lower=0.1, upper=10.0),
        draws=20000, random_seed=SEMILLA,
    )
    print(pd.DataFrame({
        "ec_priori_mediana": np.median(ec_previa),
        "ec_post_mediana": np.median(ec_post, axis=0),
        "ec_priori_sd": ec_previa.std(),
        "ec_post_sd": ec_post.std(axis=0),
    }, index=CANALES).round(2))

    print("\nAdstock contra Hill: ¿se pelean por explicar la misma curvatura?")
    print(pd.DataFrame({
        "alpha_sin_hill": np.median(sin_hill["idata"].posterior["alpha"].values.reshape(-1, len(CANALES)), axis=0),
        "alpha_con_hill": np.median(con_hill["idata"].posterior["alpha"].values.reshape(-1, len(CANALES)), axis=0),
    }, index=CANALES).round(2))

    print("\nsigma (lo que queda sin explicar):")
    for etiqueta, res in resultados.items():
        print(f"  {etiqueta}: {float(res['idata'].posterior['sigma'].mean()):.3f}")


if __name__ == "__main__":
    main()
