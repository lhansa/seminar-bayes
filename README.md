# seminar-bayes

Material del seminario **"Decidir sin certeza: una introducción a la inferencia bayesiana"**.

Las slides se publican en GitHub Pages. El seminario tiene dos partes:

1. **Teoría (~1 h).** Slides Quarto/revealjs en [`index.qmd`](index.qmd). Sigue el guion de la carta *01-inferencia-estadistica* del repositorio `estadistica-correspondencia`: la moneda (frecuentista vs. bayesiano) y el radón de Minnesota (agrupado → unpooled → jerárquico).
2. **Taller (~1 h).** Notebook de Jupyter en [`notebooks/taller.ipynb`](notebooks/taller.ipynb). Aquí no se repite el recorrido de las slides: se construye un modelo de *marketing mix* desde cero con los datos simulados de [Google Meridian](https://github.com/google/meridian), siguiendo su metodología (escalado, adstock geométrico, saturación de Hill y priori sobre el ROI en vez de sobre los coeficientes). El foco es elegir prioris y defenderlas, simular desde ellas antes de ver los datos, diagnosticar el ajuste y leer la posteriori. La versión resuelta está en [`notebooks/taller-solucion.ipynb`](notebooks/taller-solucion.ipynb), que no se publica con las slides: se entrega al terminar la sesión.

Público objetivo: profesionales de datos que manejan Python y regresión, pero no han trabajado con métodos bayesianos.

## Estructura

```
index.qmd                         slides de la parte teórica
custom.scss                       tema de las slides (morado sobre simple)
_quarto.yml                       configuración del proyecto Quarto
src/estilo.py                     estilo común de matplotlib para slides y notebook
src/mmm.py                        datos y transformaciones del taller (adstock, Hill, escalado)
data/radon.csv                    919 mediciones de radón en Minnesota (Gelman)
data/meridian_national.csv        156 semanas de marketing mix simuladas por Google (Meridian)
notebooks/taller.ipynb            taller práctico
notebooks/taller-solucion.ipynb   el taller con los nueve ejercicios resueltos
notebooks/idata/                  posteriori guardada del modelo del taller
img/                              favicon, logo y QR
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

`data/meridian_national.csv` es el conjunto simulado de Google Meridian (Apache 2.0) que usa el taller: 156 semanas, cinco canales de pago con impresiones e inversión, dos controles y las conversiones. Detalle de las columnas en [`data/README.md`](data/README.md).

El notebook del taller se ejecuta entero, muestreo incluido, en unos tres minutos. Quien vaya con prisa puede poner `MUESTREAR = False` y cargar la posteriori guardada en `notebooks/idata/`.

Lo mismo vale para `notebooks/taller-solucion.ipynb`, que es el mismo notebook con los nueve ejercicios resueltos. Los dos se commitean sin outputs y los dos quedan fuera de `_quarto.yml`: el sitio publicado son solo las slides.
