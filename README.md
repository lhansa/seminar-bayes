# seminar-bayes

Material del seminario **"Decidir sin certeza: una introducción a la inferencia bayesiana"**.

Las slides se publican en GitHub Pages. El seminario tiene dos partes:

1. **Teoría (~1 h).** Slides Quarto/revealjs en [`index.qmd`](index.qmd). Sigue el guion de la carta *01-inferencia-estadistica* del repositorio `estadistica-correspondencia`: la moneda (frecuentista vs. bayesiano) y el radón de Minnesota (agrupado → unpooled → jerárquico).
2. **Taller (~1 h).** Notebook de Jupyter en [`notebooks/taller.ipynb`](notebooks/taller.ipynb), con otro conjunto de datos. El recorrido es el mismo, pero lo monta quien asiste.

Público objetivo: profesionales de datos que manejan Python y regresión, pero no han trabajado con métodos bayesianos.

## Estructura

```
index.qmd              slides de la parte teórica
custom.scss            tema de las slides (morado sobre simple)
_quarto.yml            configuración del proyecto Quarto
src/estilo.py          estilo común de matplotlib para slides y notebook
data/radon.csv         919 mediciones de radón en Minnesota (Gelman)
notebooks/taller.ipynb esqueleto del taller práctico
img/                   favicon, logo y QR
```

## Requisitos

- Python 3.12
- [Quarto](https://quarto.org/docs/get-started/) 1.4 o superior
- `gcc`/`g++` (el backend C de PyTensor los necesita para compilar los modelos de pymc)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Renderizar en local

```bash
quarto render          # genera _site/
quarto preview         # recarga en caliente mientras editas
```

El render ejecuta varios modelos de pymc, así que la primera vez tarda unos minutos. El proyecto usa `freeze: auto`: mientras no cambie el código de una celda, Quarto reutiliza el resultado guardado en `_freeze/`.

**Conviene commitear `_freeze/`.** Así el workflow de publicación no vuelve a muestrear y el despliegue baja de minutos a segundos.

## Publicación

`.github/workflows/publish.yml` renderiza y despliega a GitHub Pages en cada push a `main`. Requiere tener configurado, en *Settings → Pages*, el origen **GitHub Actions**.

## Datos

`data/radon.csv` es el conjunto de radón de Minnesota que usan Gelman y Hill, copiado del repositorio `estadistica-correspondencia`. Columnas relevantes: `log_radon`, `floor` (0 = sótano, 1 = planta baja), `county` y `county_code`.

El conjunto de datos del taller está pendiente de decidir. Ver los issues abiertos.
