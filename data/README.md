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

## Datos del taller

Pendiente. Lo que tiene que cumplir el conjunto que elijamos:

- variable respuesta continua (o transformable, tipo logaritmo),
- al menos un predictor a nivel de observación,
- una variable de grupo con **muchos grupos y número de observaciones muy desigual entre ellos**, que es lo que hace que el modelo jerárquico se note,
- licencia que permita redistribuirlo en este repositorio,
- tamaño razonable: el MCMC tiene que terminar en minutos, no en horas.
