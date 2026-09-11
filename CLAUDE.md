# CLAUDE.md

Instrucciones para agentes que trabajen en este repositorio.

## Qué es esto

Material de un seminario sobre inferencia bayesiana, en dos partes:

- **Parte 1 (~1 h):** slides revealjs en `index.qmd`.
- **Parte 2 (~1 h):** taller práctico en `notebooks/taller.ipynb`: se construye un modelo de *marketing mix* nacional con `data/meridian_national.csv`, siguiendo la metodología de Google Meridian. El eje no es la jerarquía, es la construcción del modelo: prioris, simulación previa, diagnóstico y lectura de la posteriori.

Público: profesionales de datos. Saben Python y regresión; no saben bayesiana. Se puede dar por sabido OLS, p-valores e intervalos de confianza.

Idioma de todo el material: **español**. Los nombres de fichero, variables y ramas, en inglés o español según ya estén; no renombrar por gusto.

## Origen del contenido

El guion de la parte teórica sale de `cartas/01-inferencia-estadistica/carta.qmd` del repositorio **`estadistica-correspondencia`**, del mismo autor. Si hay que ampliar una sección de las slides, la fuente de verdad es esa carta: mismos datos, mismas prioris, mismas conclusiones. No inventes resultados nuevos ni cambies los valores de las prioris sin motivo.

`data/radon.csv` es copia del que hay en ese repositorio.

Para el taller, la fuente de verdad metodológica es el repositorio **`google/meridian`** (Apache 2.0): escalado del KPI y de los medios, adstock geométrico normalizado, saturación de Hill y, sobre todo, la priori sobre el ROI de la que se deduce `beta`. Si hay que ampliar el taller, se mira su código (`meridian/model/`), no la memoria. Sus prioris por defecto están en `meridian/model/prior_distribution.py`. El taller las usa tal cual **salvo dos**: `sigma` pasa de `HalfNormal(5)` a `Exponential(1)` y `gamma` de `Normal(0, 5)` a `Normal(0, 1)`. En un modelo nacional con 156 semanas y el KPI estandarizado, las de Meridian atribuyen ingresos negativos a más del 3 % de las semanas simuladas; está justificado en la sección 5 del notebook. `mu` sí se queda en `Normal(0, 5)`, y tiene que quedarse: el término de medios aporta casi cuatro desviaciones típicas y `mu` es quien lo compensa. No las "arregles" comparando con `prior_distribution.py`. `data/meridian_national.csv` es copia literal de su fichero `national_all_channels.csv`.

Para el estilo visual de las slides, la referencia es el repositorio **`ceu-2606`**, también del autor.

## Cómo son las slides de este autor

Esto es lo que más importa al editar `index.qmd`:

- **El título de la slide es una frase que resume la slide**, no una etiqueta. "Los condados con pocos datos se acercan a la media global", no "Shrinkage".
- **Muy poco texto en el cuerpo.** Muchas slides son solo el título. Otras, un gráfico. Otras, tres bullets como mucho.
- Las enumeraciones largas van dentro de `::: {.incremental}` para que aparezcan una a una.
- El código se muestra **a veces**: con `#| echo: true` cuando el código *es* el contenido de la slide (la definición de un modelo pymc), y oculto cuando solo genera una figura.
- `#` abre sección (slide de separación), `##` es una slide normal.
- Tono ácido y directo, con giros de guion ("¿Te has dado cuenta de lo que acabo de hacer?"). Sin relleno ni fórmulas de cortesía.

## Convenciones técnicas

- Todos los gráficos con matplotlib, aplicando `aplicar_estilo()` de `src/estilo.py`. El color de acento es `ACENTO` (morado `#800080`, el mismo del tema).
- Semilla fija: `SEMILLA = 42`.
- Modelos con `pymc`; diagnóstico y HDI con `arviz` (`az.hdi`, `az.summary`, `az.plot_ppc`).
- Rutas de datos relativas a la raíz del proyecto (`data/radon.csv`), porque Quarto ejecuta desde ahí. El notebook resuelve la raíz por su cuenta.
- El muestreo en las slides usa `draws=1000, tune=1000` (y `target_accept=0.95` en el jerárquico) para que el render no se eternice. No lo subas sin necesidad.
- El taller muestrea `draws=1000, tune=1000, chains=4, target_accept=0.97`: unos dos minutos y cero divergencias. Con `0.95` salen una o dos divergencias sueltas según la semilla, y eso pasaba ya con las prioris originales: no lo bajes. Guarda la posteriori en `notebooks/idata/modelo_meridian.nc` (solo los grupos `posterior`, `sample_stats` y `observed_data`, para que no se vaya de tamaño); la predictiva posterior se recalcula al cargarla.
- El notebook del taller se commitea **sin outputs**: lo ejecuta quien asiste.
- `notebooks/taller-solucion.ipynb` es ese mismo notebook con los nueve ejercicios resueltos, para el ponente. Es copia literal del taller salvo en tres sitios: la nota de la celda de cabecera, las nueve celdas `# Tu código aquí` y una celda markdown `**Respuesta.**` detrás de cada una. Los ids de celda compartidos son los mismos (`celda-NN`; las nuevas, `celda-NN-respuesta`), así que un diff entre los dos notebooks se lee de un vistazo. También va sin outputs y también queda fuera de `_quarto.yml`: se entrega aparte al terminar la sesión.
- `_quarto.yml` renderiza **solo** `index.qmd`. El notebook del taller queda fuera del sitio a propósito.

## Comandos

```bash
pip install -r requirements.txt
quarto render     # a _site/
quarto preview
```

El render ejecuta MCMC: la primera vez tarda un rato (unos 45 s en el runner de Actions; en local, lo que dé la máquina). `freeze: auto` guarda resultados en `_freeze/`, que **no se commitea**: el workflow de Pages cachea ese directorio por su cuenta, en el paso `Restore Quarto freeze cache` de `.github/workflows/publish.yml`.

## Al terminar un cambio

- Si tocas el código de una celda, `_freeze/` queda obsoleto para esa celda: vuelve a renderizar para comprobar que sigue saliendo lo que esperas. `_freeze/` se queda en local.
- Si tocas `notebooks/taller.ipynb` —un enunciado, una celda, el orden de las secciones—, replícalo en `notebooks/taller-solucion.ipynb`. Los dos notebooks se editan a la vez o se desincronizan en una sesión.
- Si añades dependencias, actualiza `requirements.txt`.
- Si cambias la estructura, actualiza `README.md` y este fichero.
