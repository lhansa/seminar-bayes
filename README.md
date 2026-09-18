# seminar-bayes

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lhansa/seminar-bayes/blob/main/notebooks/taller.ipynb)

Material del seminario **"Inferencia bayesiana en la empresa"**, una hora sobre los datos de *marketing mix* simulados por [Google Meridian](https://github.com/google/meridian).

Las slides se publican en GitHub Pages. El recorrido: la moneda (60 caras en 100 tiradas, frecuentista vs. bayesiano, resuelta por simulación), el esqueleto del KPI (nivel y controles), el modelo de medios (adstock geométrico y saturación de Hill) y una discusión final sobre por qué Meridian pone la priori en el ROI y no en los coeficientes. El foco son **las dos cosas que se practican mal**: elegir prioris y defenderlas simulando desde ellas antes de ver los datos, y diagnosticar lo que sale.

El seminario se está rehaciendo: `index.qmd`, las slides nuevas, está por escribir.

**Material archivado.** Del formato anterior, de dos horas, quedan en el repositorio y sin tocar las slides de teoría ([`index_radon.qmd`](index_radon.qmd): moneda y radón de Minnesota, agrupado → *unpooled* → jerárquico) y el taller de Meridian ([`notebooks/taller.ipynb`](notebooks/taller.ipynb), con los seis ejercicios resueltos en [`notebooks/taller-solucion.ipynb`](notebooks/taller-solucion.ipynb)). Nada de eso se publica con las slides.

Público objetivo: profesionales de datos que manejan Python y regresión, pero no han trabajado con métodos bayesianos.

## Estructura

```
index.qmd                         slides del seminario (por escribir)
index_radon.qmd                   slides del formato anterior, archivadas
custom.scss                       tema de las slides (morado de marca #800080 sobre simple)
_quarto.yml                       configuración del proyecto Quarto
src/estilo.py                     estilo común de matplotlib para las slides
data/radon.csv                    919 mediciones de radón en Minnesota (Gelman), de las slides archivadas
data/meridian_national.csv        156 semanas de marketing mix simuladas por Google (copia offline; el material las lee por URL)
notebooks/taller.ipynb            taller archivado
notebooks/taller-solucion.ipynb   el taller archivado, con los ejercicios resueltos
notebooks/idata/                  posteriori del modelo de medios, guardada a mano (no la usa nadie)
img/                              favicon, logo y QR
.devcontainer/                    entorno de las slides en Codespaces (Quarto, compilador y venv con uv)
```

## Antes de la sesión

Hay dos maneras de llegar al taller archivado con el entorno listo. La corta:

**Google Colab.** Abre el badge de arriba, ejecuta la primera celda y ya está. Esa celda instala `numpy`, `pymc` y `arviz` con los mismos topes que `requirements.txt`, y no hace nada más: el notebook es autosuficiente y lee los datos por URL del repositorio de Meridian, así que no clona nada ni importa nada de `src/`. No hace falta cuenta de GitHub ni compilador: el runtime de Colab ya trae `gcc`. Si Colab pide reiniciar el entorno después de instalar, se reinicia y se vuelve a empezar por la primera celda.

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

Los terminales nuevos arrancan con el venv activado, y Quarto usa su intérprete aunque no lo esté: `QUARTO_PYTHON` apunta a `.venv/bin/python`. El Codespace es para las slides; el taller archivado se abre en Colab.

La versión de Quarto va fijada en una variable al principio de `post-create.sh`; para actualizarla, esa línea y nada más. Si algo falla durante la creación, el contenedor arranca igual y el error se lee en el terminal: el script se puede relanzar con `bash .devcontainer/post-create.sh` tantas veces como haga falta.

## Publicación

`.github/workflows/publish.yml` renderiza y despliega a GitHub Pages en cada push a `main`. Requiere tener configurado, en *Settings → Pages*, el origen **GitHub Actions**.

## Datos

`data/radon.csv` es el conjunto de radón de Minnesota que usan Gelman y Hill, copiado del repositorio `estadistica-correspondencia`. Columnas relevantes: `log_radon`, `floor` (0 = sótano, 1 = planta baja), `county` y `county_code`.

`data/meridian_national.csv` es el conjunto simulado de Google Meridian (Apache 2.0) del seminario: 156 semanas, cinco canales de pago con impresiones e inversión, dos controles y las conversiones. Detalle de las columnas en [`data/README.md`](data/README.md). El notebook no lee esta copia: descarga los datos del repositorio de Meridian fijando el tag `v1.1.5`, que sirve un fichero idéntico. La copia se queda aquí como red de seguridad si algún día esa URL deja de responder.

El notebook del taller se ejecuta entero, con los dos muestreos dentro, en poco más de dos minutos: el esqueleto ajusta en tres segundos y el modelo de medios en poco más de un minuto. En Colab, que va más justo de CPU, cuenta con algo más. En `notebooks/idata/` hay una posteriori del modelo de medios guardada a mano; el notebook ni la escribe ni la lee, y está ahí para quien quiera mirarla sin esperar al muestreo.

Los dos notebooks se commitean sin outputs y los dos quedan fuera de `_quarto.yml`: el sitio publicado son solo las slides.
