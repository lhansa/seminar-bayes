# seminar-bayes

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lhansa/seminar-bayes/blob/main/notebooks/taller.ipynb)

Material del seminario **"Decidir sin certeza: una introducción a la inferencia bayesiana"**.

Las slides se publican en GitHub Pages. El seminario tiene dos partes:

1. **Teoría (~1 h).** Slides Quarto/revealjs en [`index.qmd`](index.qmd). Sigue el guion de la carta *01-inferencia-estadistica* del repositorio `estadistica-correspondencia`, con recortes: arranca con la moneda (frecuentista vs. bayesiano, resuelta por simulación) y sigue con el radón de Minnesota (agrupado → unpooled → jerárquico).
2. **Taller (~1 h).** Notebook de Jupyter en [`notebooks/taller.ipynb`](notebooks/taller.ipynb). Aquí no se repite el recorrido de las slides: se construyen **dos modelos** de *marketing mix* sobre los datos simulados de [Google Meridian](https://github.com/google/meridian), siguiendo su metodología (escalado, adstock geométrico y priori sobre el ROI en vez de sobre los coeficientes). Primero el esqueleto —nivel y controles, tres prioris, ajusta en segundos— y luego el modelo con los cinco canales de medios. El foco son **las dos cosas que se practican mal**: elegir prioris y defenderlas simulando desde ellas antes de ver los datos, y diagnosticar lo que sale. Seis ejercicios: tres de prioris, dos de diagnóstico y uno de decisión. La versión resuelta está en [`notebooks/taller-solucion.ipynb`](notebooks/taller-solucion.ipynb), que no se publica con las slides: se entrega al terminar la sesión.

Público objetivo: profesionales de datos que manejan Python y regresión, pero no han trabajado con métodos bayesianos.

## Estructura

```
index.qmd                         slides de la parte teórica
custom.scss                       tema de las slides (morado de marca #800080 sobre simple)
_quarto.yml                       configuración del proyecto Quarto
src/estilo.py                     estilo común de matplotlib para slides y notebook
src/mmm.py                        datos y transformaciones del taller (escalado, adstock; Hill sin usar)
data/radon.csv                    919 mediciones de radón en Minnesota (Gelman)
data/meridian_national.csv        156 semanas de marketing mix simuladas por Google (Meridian)
notebooks/taller.ipynb            taller práctico
notebooks/taller-solucion.ipynb   el taller con los seis ejercicios resueltos
notebooks/idata/                  posteriori guardada del modelo de medios del taller
img/                              favicon, logo y QR
.devcontainer/                    entorno de las slides en Codespaces (Quarto, compilador y venv con uv)
```

## Antes de la sesión

Hay dos maneras de llegar al taller con el entorno listo. La corta:

**Google Colab.** Abre el badge de arriba, ejecuta la primera celda y ya está. Esa celda instala `numpy`, `pymc`, `arviz` y `h5netcdf` con los mismos topes que `requirements.txt` y clona este repositorio en `/content/seminar-bayes`, así que el notebook encuentra los datos, `src/` y la posteriori guardada igual que en local. No hace falta cuenta de GitHub ni compilador: el runtime de Colab ya trae `gcc`. Si Colab pide reiniciar el entorno después de instalar, se reinicia y se vuelve a empezar por la primera celda.

**En local.** Lo que viene a continuación. Quarto solo hace falta para las slides; para el taller basta con Python y `requirements.txt`.

Las versiones van fijadas a propósito: `pymc 6` exige `arviz 1.x`, que cambia la API de `az.summary`, `az.plot_ppc` y compañía, y este material está escrito contra `arviz 0.x`.

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

El render ejecuta varios modelos de pymc, así que la primera vez tarda un rato: unos 45 s en el runner de GitHub, y lo que dé tu máquina en local. El proyecto usa `freeze: auto`: mientras no cambie el código de una celda, Quarto reutiliza el resultado guardado en `_freeze/`.

**`_freeze/` no se commitea.** El workflow de publicación cachea ese directorio entre ejecuciones, así que tampoco vuelve a muestrear salvo que cambie el código de una celda o caduque la caché.

## Las slides en un Codespace

Quien no quiera instalar nada en su máquina puede abrir el repositorio en un Codespace: *Code → Codespaces → Create codespace on main*. La imagen es `mcr.microsoft.com/devcontainers/base:ubuntu-24.04`, el mismo Ubuntu que usa el workflow de publicación, y al crearse el contenedor `post-create.sh` instala el compilador, Quarto, [`uv`](https://docs.astral.sh/uv/) y el venv con `requirements.txt`. Tarda un par de minutos. Cuando termina:

```bash
quarto render                  # genera _site/
quarto preview --port 4200     # ese puerto ya viene reenviado
```

Los terminales nuevos arrancan con el venv activado, y Quarto usa su intérprete aunque no lo esté: `QUARTO_PYTHON` apunta a `.venv/bin/python`. El Codespace es para las slides; el taller se sigue haciendo en Colab.

La versión de Quarto va fijada en una variable al principio de `post-create.sh`; para actualizarla, esa línea y nada más. Si algo falla durante la creación, el contenedor arranca igual y el error se lee en el terminal: el script se puede relanzar con `bash .devcontainer/post-create.sh` tantas veces como haga falta.

## Publicación

`.github/workflows/publish.yml` renderiza y despliega a GitHub Pages en cada push a `main`. Requiere tener configurado, en *Settings → Pages*, el origen **GitHub Actions**.

## Datos

`data/radon.csv` es el conjunto de radón de Minnesota que usan Gelman y Hill, copiado del repositorio `estadistica-correspondencia`. Columnas relevantes: `log_radon`, `floor` (0 = sótano, 1 = planta baja), `county` y `county_code`.

`data/meridian_national.csv` es el conjunto simulado de Google Meridian (Apache 2.0) que usa el taller: 156 semanas, cinco canales de pago con impresiones e inversión, dos controles y las conversiones. Detalle de las columnas en [`data/README.md`](data/README.md).

El notebook del taller se ejecuta entero, con los dos muestreos dentro, en poco más de dos minutos: el esqueleto ajusta en tres segundos y el modelo de medios en poco más de un minuto. Quien vaya con prisa puede poner `MUESTREAR = False` en la sección 5 y cargar la posteriori guardada en `notebooks/idata/`. En Colab esa posteriori llega con el clon del repositorio, así que la vía corta también funciona allí.

Lo mismo vale para `notebooks/taller-solucion.ipynb`, que es el mismo notebook con los seis ejercicios resueltos. Los dos se commitean sin outputs y los dos quedan fuera de `_quarto.yml`: el sitio publicado son solo las slides.
