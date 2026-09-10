# Datos

## `radon.csv`

919 mediciones de radón en viviendas de 85 condados de Minnesota. Es el conjunto que usan Gelman y Hill en *Data Analysis Using Regression and Multilevel/Hierarchical Models* y en *Regression and Other Stories*.

Copiado del repositorio `estadistica-correspondencia`, donde se usa en la carta *01-inferencia-estadistica*.

Columnas que usan las slides:

| Columna | Descripción |
|---|---|
| `log_radon` | logaritmo de la medición de radón (pCi/L) |
| `floor` | planta de la medición: 0 = sótano, 1 = planta baja |
| `county` | nombre del condado |
| `county_code` | índice entero del condado, 0–84, para indexar en pymc |
| `Uppm` | uranio del suelo en el condado. Sin usar; encaja como predictor de nivel condado |

## `meridian_national.csv`

Datos simulados de [Google Meridian](https://github.com/google/meridian), la librería de
*marketing mix modeling* de Google. Copia literal de
`meridian/data/simulated_data/csv/national_all_channels.csv`, publicado bajo licencia
Apache 2.0, que permite redistribuirlo citando origen y licencia.

156 semanas, del 2021-01-25 al 2024-01-15, a nivel nacional (una sola serie, sin
regiones).

| Columna | Descripción |
|---|---|
| `time` | semana |
| `conversions` | conversiones de la semana |
| `revenue_per_conversion` | ingreso medio por conversión |
| `Channel0..4_impression` | impresiones de cada canal de pago |
| `Channel0..4_spend` | inversión en cada canal, en euros |
| `Organic_channel0_impression` | impresiones de un canal orgánico. Sin usar en el taller |
| `competitor_sales_control` | control: ventas de la competencia |
| `sentiment_score_control` | control: sentimiento de marca |
| `Promo` | intensidad promocional. Sin usar en el taller |

El KPI del taller son los **ingresos**: `revenue = conversions * revenue_per_conversion`.
Así el ROI queda en euros por euro y la priori que Meridian pone por defecto sobre el ROI,
`LogNormal(0.2, 0.9)`, se puede usar tal cual. La columna la añade `cargar_datos()` en
`src/mmm.py`.

En el mismo directorio del repositorio de Meridian hay versiones **por regiones**
(`geo_all_channels.csv` y compañía), que son las que piden un modelo jerárquico. El taller
las menciona pero usa la nacional: la segunda hora del seminario va de construir un
modelo, no de repetir el shrinkage de las slides.
