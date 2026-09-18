# CLAUDE.md

Instrucciones para agentes que trabajen en este repositorio.

## Qué es esto

Seminario de **una hora** sobre inferencia bayesiana en la empresa: slides revealjs en `index.qmd`, sobre los datos de *marketing mix* de Google Meridian. Recorrido, **tres bloques**:

1. **La moneda.** 60 caras en 100 tiradas, el p-valor por simulación y la vuelta al problema.
2. **El esqueleto.** Meridian nacional sin medios: nivel y controles del KPI, tres prioris, simulación previa, muestreo y diagnóstico. Ajusta en tres segundos.
3. **El modelo de medios.** Adstock geométrico normalizado, la priori sobre el ROI en lugar de sobre `beta`, y el mismo bucle otra vez.

Por qué Meridian pone la priori en el ROI y no en `beta` **se implementa**, no se discute al final: es el bloque 3.

El eje no es el *marketing mix*: son **elegir prioris y diagnosticar**, y por eso el bucle priori → simulación previa → ajuste → diagnóstico se recorre entero dos veces, en el esqueleto y en los medios. Es una hora: si hay que añadir algo, se quita otra cosa.

Público: profesionales de datos. Saben Python y regresión; no saben bayesiana. Se puede dar por sabido OLS, p-valores e intervalos de confianza.

Idioma de todo el material: **español**. Los nombres de fichero, variables y ramas, en inglés o español según ya estén; no renombrar por gusto.

**`index.qmd` está por escribir**: el seminario se rehace entero (issue #36). `_quarto.yml` ya apunta a él y no renderiza nada más, así que hasta que exista el render falla.

## Material archivado

Se queda en el repositorio y **no se toca** salvo que un issue lo pida. Es la cantera de la charla nueva, no material a mantener al día:

- `index_radon.qmd`: las slides del seminario anterior, de dos horas, con la moneda y el radón de Minnesota (agrupado → *unpooled* → jerárquico). De aquí sale la parte de la moneda, y de aquí sale también el recorrido de `notebooks/radon.ipynb`.
- `notebooks/taller.ipynb` y `notebooks/taller-solucion.ipynb`: el taller de Meridian que ya no se imparte. De aquí sale el código de los bloques 2 y 3, el modelo de medios incluido.
- `notebooks/idata/modelo_meridian.nc`.

`data/radon.csv` **no** es material archivado: lo lee `notebooks/radon.ipynb`.

Nada de eso entra en `_quarto.yml`.

## Origen del contenido

La parte de la moneda sale de `cartas/01-inferencia-estadistica/carta.qmd` del repositorio **`estadistica-correspondencia`**, del mismo autor, vía `index_radon.qmd`. Esa carta es la fuente de verdad: mismos datos, mismas prioris, mismas conclusiones. No inventes resultados ni cambies los valores de las prioris sin motivo.

Las diferencias con la carta son decisiones tomadas, no olvidos, y se mantienen: la anécdota de Obama con la que abre la carta se ha quitado (se empieza con la moneda), la moneda se resuelve solo por simulación (fuera la aproximación normal y el binomial exacto) y la posteriori exacta (una Beta) también se queda fuera: el aside da la forma proporcional de Bayes, que es lo que explica por qué se puede muestrear sin la constante normalizadora.

**Las dos slides del muestreo llevan un Metropolis a mano, en numpy, y es a propósito** (issue #29). NUTS da muestras casi independientes: su recorrido parece ruido blanco y no se ve ni un paso corto ni un rechazo, que es justo lo que ahí se cuenta de palabra. Por lo mismo, la primera enseña solo los `zoom = 200` primeros pasos de los dos mil —con los dos mil no se distingue ninguno— y la segunda sí los enseña todos, porque ahí lo que importa ya no es el paso sino el montón. Una nota del ponente avisa de que PyMC usa NUTS y no esto.

La fuente de verdad metodológica del modelo es el repositorio **`google/meridian`** (Apache 2.0): escalado del KPI y de los medios, adstock geométrico normalizado, la priori sobre el ROI y, si acaba entrando, la saturación de Hill. Si hay que ampliar algo, se mira su código (`meridian/model/`), no la memoria.

Los datos se leen **por URL**, fijando el tag `v1.1.5`:
`raw.githubusercontent.com/google/meridian/v1.1.5/meridian/data/simulated_data/csv/national_all_channels.csv`. El tag es el punto: **no lo cambies a `main`**. Fijado, el fichero es inmutable; en `main`, un `git mv` de Google revienta el material un martes por la tarde con la sala llena. `data/meridian_national.csv` se queda como red de seguridad offline: es byte a byte el mismo fichero.

## Decisiones del modelo

- Las prioris por defecto de Meridian están en `meridian/model/prior_distribution.py`. Se usan tal cual **salvo dos**: `sigma` pasa de `HalfNormal(5)` a `Exponential(1)` y `gamma` de `Normal(0, 5)` a `Normal(0, 1)`. En un modelo nacional con 156 semanas y el KPI estandarizado, las de Meridian generan ingresos semanales negativos; eso se mide con la simulación previa, no se cuenta.
- **`mu` cambia entre los dos modelos y no es un descuido**: `Normal(0, 1)` en el esqueleto, donde es el nivel de un KPI estandarizado, y `Normal(0, 5)` en el de medios, donde tiene que compensar lo que aportan (su posteriori se va a −2,8; con la otra priori no llegaría). Ese cambio *es* la lección del bloque 3, así que no lo unifiques ni lo "arregles" comparando con `prior_distribution.py`.
- **`beta` no lleva priori: es determinista.** La priori va sobre el ROI, `roi ~ LogNormal(0,2; 0,9)`, y `beta` se deduce de ella: `beta_m = roi_m · gasto_m / (sd(y) · Σ_t adstock_tm)`. El adstock lleva `alpha ~ Uniform(0, 1)`. Nadie tiene intuición sobre el coeficiente de una inversión rezagada, dividida por su mediana, sobre un KPI estandarizado; sobre el ROI sí la tiene el equipo de marketing, y por eso la priori se pone ahí. Es la decisión de Meridian y la del taller archivado: **la misma**, no dos decisiones de dos formatos.
- **La saturación de Hill está por decidir, y la decide otro issue** con la simulación previa y el muestreo delante, no la memoria. Hasta entonces, el modelo de la charla va **sin Hill**; no la metas por tu cuenta. Lo que ya se sabe: cuesta un parámetro más por canal y se pelea con el adstock por explicar la misma forma, así que con ella el muestreo pedía `target_accept=0.97` y sin ella bastaba `0.9`.

## Cómo son las slides de este autor

Esto es lo que más importa al editar `index.qmd`:

- **El título de la slide es una frase que resume la slide**, no una etiqueta. "Los canales con poca inversión se acercan a la media", no "Shrinkage".
- **Muy poco texto en el cuerpo.** Muchas slides son solo el título. Otras, un gráfico. Otras, tres bullets como mucho.
- Las enumeraciones largas van dentro de `::: {.incremental}` para que aparezcan una a una.
- El código se muestra **a veces**: con `#| echo: true` cuando el código *es* el contenido de la slide (la definición de un modelo pymc), y oculto cuando solo genera una figura.
- `#` abre sección (slide de separación), `##` es una slide normal.
- Tono ácido y directo, con giros de guion ("¿Te has dado cuenta de lo que acabo de hacer?"). Sin relleno ni fórmulas de cortesía.

## Convenciones técnicas

- Todos los gráficos con matplotlib. Las **slides** aplican `aplicar_estilo()` de `src/estilo.py`; los **notebooks** llevan su propio bloque de `rcParams` en `celda-01`, que es la versión corta del mismo estilo, porque tienen que funcionar en Colab sin clonar el repositorio. El color de acento es `ACENTO` (morado `#800080`, el mismo del tema).
- **El morado `#800080` es el color de marca** y está en cinco sitios: `$morado` en `custom.scss`, `ACENTO` en `src/estilo.py` y `ACENTO` en la primera celda de cada uno de los tres notebooks. Si cambia la marca, se cambia ahí y en ningún sitio más. Las copias de fuera del `.scss` son el precio de que los notebooks no dependan de `src/` —el taller archivado porque se abre en Colab sin clonar nada, el del radón para no tocar `sys.path` desde `notebooks/`—, y es un precio aceptado.
- Dos decisiones que no son olvidos: las slides tienen **fondo blanco también las de sección** (`#`), que se distinguen por un filete bajo el título, porque al proyectar el blanco gana; y la escala `GRISES` de las figuras **se queda gris**, porque el morado marca lo que importa en cada gráfico y si se moradea la serie entera deja de marcar nada. Lo único de marca en las figuras es el cromo: `REJILLA` y el color del título de los ejes.
- El estilo visual salió del repositorio **`ceu-2606`**, también del autor (tema `simple`, títulos morados, sombra dura en las imágenes), pero de ahí en adelante este repositorio va por delante: su `custom.scss` deja el cromo en los defaults del tema y el de aquí no, porque el seminario se proyecta con la marca personal (issue #25). Los enlaces, la barra de progreso, la portada y los filetes de tabla son morados a propósito.
- El contador de slide se quitó (issue #27): `slide-number` va a `false` en el frontmatter **y** en `_quarto.yml`, porque está duplicado y gana el primero. `custom.scss` ya no lo estiliza; no lo devuelvas.
- Las etiquetas de celda **no llevan los prefijos `fig-` ni `tbl-`**: van como `graf-…` y `tabla-…`. Esos dos prefijos hacen la celda referenciable en Quarto, y una celda referenciable arrastra un caption con "Figure 1" o "Table 1" aunque no se le ponga `fig-cap` (issue #27). Ninguna figura se referencia con `@`.
- Semilla fija: `SEMILLA = 42`. Modelos con `pymc`; diagnóstico y HDI con `arviz` (`az.hdi`, `az.summary`, `az.plot_ppc`).
- Rutas de datos relativas a la raíz del proyecto, porque Quarto ejecuta desde ahí.
- El muestreo de las slides usa `draws=2000, tune=2000, chains=4`. Las slides se proyectan ya renderizadas, no se ejecutan delante de nadie: **no bajes el muestreo para ahorrar minutos de CI**. Si el render tarda, que tarde; con `freeze: auto` solo tarda una vez.
- El pin `pymc<6` de `requirements.txt` es deliberado: pymc 6 exige `arviz 1.x`, que rompe `az.summary`, `az.plot_trace`, `az.plot_ppc` y `az.from_netcdf` tal como se usan aquí. No lo "actualices"; migrar a arviz 1 es otro trabajo.
- Los notebooks se commitean **sin outputs**.

## El notebook del radón

`notebooks/radon.ipynb` **no es material de la charla**: es el regalo de suscripción. Recorre el radón de Minnesota (agrupado → *unpooled* → jerárquico), el mismo camino que `index_radon.qmd`, y existe para grabar un vídeo con él ya ejecutado.

- Es **narrativo y sin ejercicios**. No hay celdas `# Tu código aquí`, no hay notebook de soluciones y no hay pareja que mantener sincronizada: lo que en el taller archivado es un ejercicio, aquí es texto que responde a la pregunta. No copies la estructura del taller.
- Lee `data/radon.csv` **por ruta relativa** (`../data/radon.csv` desde `notebooks/`), no por URL. Se ejecuta con el repositorio clonado delante, así que **no es autosuficiente en Colab** y no lleva celda de instalación: el entorno es `requirements.txt`.
- Lleva su propio bloque de `rcParams` en la primera celda, la versión corta del estilo de `src/estilo.py`, con `ACENTO` y `GRISES`. No importa nada de `src/` ni toca `sys.path`: desde `notebooks/` eso serían tres líneas de fontanería para ahorrar diez de estilo.
- `SEMILLA = 42`, modelos con `pymc`, diagnóstico con `arviz`, como el resto del material.
- Se commitea **sin outputs**, igual que los del taller. El vídeo se graba ejecutándolo; el repositorio no guarda esa ejecución.
- Fuera de `_quarto.yml`: no se publica con las slides.

## Convenciones del taller archivado

Solo importan si un issue manda tocarlo o reaprovecharlo:

- Los dos notebooks se editan a la vez o se desincronizan: `taller-solucion.ipynb` es copia literal del otro salvo la nota de cabecera, las seis celdas `# Tu código aquí` y una celda markdown `**Respuesta.**` detrás de cada una. Los ids compartidos son los mismos (`celda-NN`; las nuevas, `celda-NN-respuesta`), para que el diff entre ambos se lea de un vistazo. El id `celda-00b` se sale de la secuencia a propósito: renumerar 45 celdas para colar una al principio hace el diff ilegible.
- El notebook es **autosuficiente** (issue #34): `celda-00b` detecta Colab e instala `numpy`, `pymc` y `arviz` con los topes de `requirements.txt`, y nada más. No clona el repositorio, no hace `%cd`, no toca `sys.path` y no importa nada de `src/`. Debe poder ejecutarse desde cualquier directorio.
- **No hay funciones de fontanería, y es a propósito.** El escalado del KPI, el de los controles, el de los medios y la matriz de rezagos se escriben inline: son dos o tres líneas de aritmética y el asistente ha venido a verlas. Las tres que quedan se ganan el sitio: `pesos_adstock()` se reutiliza en tres celdas y funciona con numpy y con pytensor a la vez, y `construir_esqueleto()` e `ingresos_previos()` existen porque el ejercicio 1 *es* llamarlas cinco veces con prioris distintas.
- **Siempre muestrea**: no hay `MUESTREAR = False` ni se lee `notebooks/idata/`. El `.nc` sigue ahí para quien quiera mirarlo, pero ninguna celda lo regenera; si hace falta rehacerlo, se ejecuta el modelo y se guarda a mano con `idata.to_netcdf(ruta, groups=["posterior", "sample_stats", "observed_data"])`. Por eso `h5netcdf` sigue en `requirements.txt`.

## Comandos

```bash
pip install -r requirements.txt
quarto render     # a _site/
quarto preview
```

`.devcontainer/` levanta ese mismo entorno en un Codespace, y lo hace **todo en `post-create.sh`**, nada en la construcción de la imagen: un build que falla manda el Codespace a modo recuperación, que arranca una imagen ajena (Alpine) y sobrescribe el log en el siguiente arranque, mientras que un fallo en `post-create.sh` deja el contenedor en pie y el error a la vista. Por eso no hay *features* ni `Dockerfile`: solo `base:ubuntu-24.04` —el mismo Ubuntu del runner de Actions, con Python 3.12 de serie— y un script reejecutable que instala `build-essential`, `python3-dev` y `libopenblas-dev` para el backend C de PyTensor, el `.deb` de Quarto con la versión fijada en una variable, `uv` desde su release, y el venv con `requirements.txt`. `QUARTO_PYTHON` apunta a ese venv. `requirements.txt` es la única lista de dependencias: no hay `pyproject.toml` ni `uv.lock` que mantener en paralelo.

El render ejecuta MCMC, así que la primera vez tarda un rato. `freeze: auto` guarda resultados en `_freeze/`, que **no se commitea**: el workflow de Pages cachea ese directorio en el paso `Restore Quarto freeze cache` de `.github/workflows/publish.yml`. Ese paso **no tiene `restore-keys` a propósito**, y tampoco lo necesita: Quarto invalida `_freeze/` por el hash del código de la celda, no por lo que la celda importa, así que un cambio en `src/` no lo toca y una caché restaurada por prefijo publicaría las figuras viejas. Por lo mismo, **si tocas `src/estilo.py` borra `_freeze/` en local** antes de volver a renderizar, o no verás el cambio.

## Al terminar un cambio

- Si tocas el código de una celda, vuelve a renderizar: `_freeze/` queda obsoleto para esa celda.
- Si añades dependencias, actualiza `requirements.txt`.
- Si cambias la estructura, actualiza `README.md` y este fichero.
- La PR se escribe sobre `.github/pull_request_template.md` y **empieza por `Fixes #NN`**. La palabra clave va en inglés (`Fixes`, `Closes`, `Resolves`): con "Cierra #NN" el issue se queda abierto después del merge, porque GitHub no la reconoce. Si la PR cierra varios issues, cada uno lleva la suya: `Fixes #12, closes #13`.
