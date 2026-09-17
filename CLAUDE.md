# CLAUDE.md

Instrucciones para agentes que trabajen en este repositorio.

## Qué es esto

Material de un seminario sobre inferencia bayesiana, en dos partes:

- **Parte 1 (~1 h):** slides revealjs en `index.qmd`.
- **Parte 2 (~1 h):** taller práctico en `notebooks/taller.ipynb`, con `data/meridian_national.csv` y la metodología de Google Meridian. Son **dos modelos**: primero el esqueleto (nivel y controles, tres prioris, muestrea en tres segundos) y luego el de medios (adstock y priori sobre el ROI). El eje no es la jerarquía, ni siquiera el *marketing mix*: son **elegir prioris y diagnosticar**, y por eso el bucle priori → simulación previa → ajuste → diagnóstico se recorre entero dos veces. Seis ejercicios: tres de prioris, dos de diagnóstico y uno de decisión, y ni uno de fontanería. Es material para las dos de la tarde: si hay que añadir algo, se quita otra cosa.

Público: profesionales de datos. Saben Python y regresión; no saben bayesiana. Se puede dar por sabido OLS, p-valores e intervalos de confianza.

Idioma de todo el material: **español**. Los nombres de fichero, variables y ramas, en inglés o español según ya estén; no renombrar por gusto.

## Origen del contenido

El guion de la parte teórica sale de `cartas/01-inferencia-estadistica/carta.qmd` del repositorio **`estadistica-correspondencia`**, del mismo autor. Si hay que ampliar una sección de las slides, la fuente de verdad es esa carta: mismos datos, mismas prioris, mismas conclusiones. No inventes resultados nuevos ni cambies los valores de las prioris sin motivo.

Las slides **no siguen la carta al pie de la letra**, y las diferencias son decisiones tomadas, no olvidos: la anécdota de Obama con la que abre la carta se ha quitado (las slides empiezan con la moneda), la moneda se resuelve solo por simulación (fuera la aproximación normal y el binomial exacto) y la comprobación predictiva previa se cuenta de palabra, sin gráfico, porque el taller la hace entera. No las restaures por parecerse más a la carta.

**Las dos slides del muestreo (issue #29) llevan un Metropolis a mano, en numpy, y es a propósito.** No se sustituye por la cadena de `idata_moneda`: NUTS da muestras casi independientes, así que su recorrido parece ruido blanco y no se ve ni un paso corto ni un rechazo, que es justo lo que ahí se cuenta de palabra. Por lo mismo, la primera de las dos enseña solo los `zoom = 200` primeros pasos de los dos mil —con los dos mil no se distingue ninguno— y la segunda sí los enseña todos, porque ahí lo que importa ya no es el paso sino el montón. Una nota del ponente avisa de que PyMC usa NUTS y no esto. La posteriori exacta (una Beta) se queda fuera, como el binomial exacto: el aside da la forma proporcional de Bayes, que es lo que explica por qué se puede muestrear sin la constante normalizadora.

`data/radon.csv` es copia del que hay en ese repositorio.

Para el taller, la fuente de verdad metodológica es el repositorio **`google/meridian`** (Apache 2.0): escalado del KPI y de los medios, adstock geométrico normalizado y, sobre todo, la priori sobre el ROI de la que se deduce `beta`. Si hay que ampliar el taller, se mira su código (`meridian/model/`), no la memoria.

**La saturación de Hill se queda fuera a propósito.** Cuesta diez minutos de explicación que no tiene nada de bayesiana y un parámetro más por canal, y es la que obligaba a subir `target_accept` a `0.97`: peleándose con el adstock por explicar la misma forma. Sin ella el modelo muestrea limpio con `0.9`. `hill()` sigue en `src/mmm.py` aunque el taller no la use, porque el notebook se la ofrece a quien quiera seguir en casa: ni la borres ni la devuelvas al modelo.

Las prioris por defecto de Meridian están en `meridian/model/prior_distribution.py`. El taller las usa tal cual **salvo dos**: `sigma` pasa de `HalfNormal(5)` a `Exponential(1)` y `gamma` de `Normal(0, 5)` a `Normal(0, 1)`. En un modelo nacional con 156 semanas y el KPI estandarizado, las de Meridian generan ingresos semanales negativos; el ejercicio 1 lo mide en vez de contarlo. `mu` es el caso interesante y **la diferencia entre los dos modelos no es un descuido**: vale `Normal(0, 1)` en el esqueleto, donde es el nivel de un KPI estandarizado, y `Normal(0, 5)` en el modelo de medios, donde tiene que compensar lo que aportan (su posteriori se va a −2,8; con la priori del esqueleto no llegaría). Ese cambio *es* la lección de la sección 4, así que no lo unifiques ni lo "arregles" comparando con `prior_distribution.py`. `data/meridian_national.csv` es copia literal de su fichero `national_all_channels.csv`.

Para el estilo visual de las slides, el punto de partida fue el repositorio **`ceu-2606`**, también del autor: tema `simple`, títulos morados y la sombra dura de las imágenes. De ahí en adelante este repositorio va por delante. El `custom.scss` de `ceu-2606` define una sola variable y deja el resto del cromo en los defaults del tema; el de aquí no, porque el seminario se proyecta con la marca personal (issue #25). No lo "arregles" comparándolo con el de allí: los enlaces, la barra de progreso, la portada y los filetes de tabla son morados a propósito. El contador de slide se quitó en el issue #27, así que `slide-number` va a `false` —en el frontmatter de `index.qmd` **y** en `_quarto.yml`, porque está duplicado y gana el primero— y `custom.scss` ya no lo estiliza: no lo devuelvas.

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
- **El morado `#800080` es el color de marca** y está en dos sitios: como variable `$morado` en `custom.scss` y como `ACENTO` en `src/estilo.py`. Si cambia la marca, se cambia en esos dos y en ninguno más. Dos decisiones que no son olvidos: las slides tienen **fondo blanco también las de sección** (`#`), que se distinguen por un filete bajo el título y no por invertir el fondo, porque al proyectar el blanco gana; y la escala `GRISES` de las figuras **se queda gris**, porque el morado marca lo que importa en cada gráfico y si se moradea la serie entera deja de marcar nada. Lo único de marca en las figuras es el cromo: `REJILLA` y el color del título de los ejes.
- Las etiquetas de celda de `index.qmd` **no llevan los prefijos `fig-` ni `tbl-`**: van como `graf-…` y `tabla-…`. Esos dos prefijos son los que hacen la celda referenciable en Quarto, y una celda referenciable arrastra un caption con "Figure 1" o "Table 1" aunque no se le ponga `fig-cap` (issue #27). Ninguna figura de las slides se referencia con `@`, así que no hacen falta.
- Semilla fija: `SEMILLA = 42`.
- Modelos con `pymc`; diagnóstico y HDI con `arviz` (`az.hdi`, `az.summary`, `az.plot_ppc`).
- Rutas de datos relativas a la raíz del proyecto (`data/radon.csv`), porque Quarto ejecuta desde ahí. El notebook resuelve la raíz por su cuenta.
- El muestreo en las slides usa `draws=1000, tune=1000` (y `target_accept=0.95` en el jerárquico) para que el render no se eternice. No lo subas sin necesidad.
- El taller muestrea **dos veces**. El esqueleto, con `draws=1000, tune=1000, chains=4` y nada más: tres segundos, cero divergencias. El modelo de medios, lo mismo más `target_accept=0.9`: unos 67 segundos, cero divergencias, `r_hat` 1,00 y `ess_bulk` mínimo por encima de 2.300. El notebook entero, de la primera celda a la última, tarda algo más de dos minutos. Solo se guarda la posteriori del modelo de medios, en `notebooks/idata/modelo_meridian.nc` (grupos `posterior`, `sample_stats` y `observed_data`); la predictiva posterior se recalcula al cargarla. El esqueleto no se guarda: tarda menos en ajustarse que en leerse del disco, y que ajuste en directo es parte de la gracia.
- El notebook del taller se commitea **sin outputs**: lo ejecuta quien asiste.
- El taller está pensado para abrirse en **Google Colab** (badge en el README) y seguir funcionando en local sin cambiar nada. De eso se encarga `celda-00b`, la primera celda de código: detecta Colab, instala `numpy`, `pymc`, `arviz` y `h5netcdf` con los mismos topes que `requirements.txt`, clona el repositorio en `/content/seminar-bayes` y hace `%cd` a su `notebooks/`. Ese `%cd` es lo que permite que `celda-01` quede byte-idéntica: la raíz se sigue deduciendo de `Path.cwd().name == "notebooks"`, y con ella los datos, `src/` y `notebooks/idata/`. Si tocas el arranque, no toques `celda-01`.
- El id `celda-00b` se sale de la secuencia `celda-NN` a propósito: renumerar las 45 celdas para colar una al principio convierte el diff entre los dos notebooks en ilegible.
- El pin `pymc<6` de `requirements.txt` y el de `celda-00b` son deliberados: pymc 6 exige `arviz 1.x`, que rompe `az.summary`, `az.plot_trace`, `az.plot_ppc` y `az.from_netcdf` tal como los usan las slides y el taller. No lo "actualices"; migrar a arviz 1 es otro trabajo.
- `notebooks/taller-solucion.ipynb` es ese mismo notebook con los seis ejercicios resueltos, para el ponente. Es copia literal del taller salvo en tres sitios: la nota de la celda de cabecera, las seis celdas `# Tu código aquí` y una celda markdown `**Respuesta.**` detrás de cada una. Los ids de celda compartidos son los mismos (`celda-NN`; las nuevas, `celda-NN-respuesta`), así que un diff entre los dos notebooks se lee de un vistazo. También va sin outputs y también queda fuera de `_quarto.yml`: se entrega aparte al terminar la sesión.
- `_quarto.yml` renderiza **solo** `index.qmd`. El notebook del taller queda fuera del sitio a propósito.

## Comandos

```bash
pip install -r requirements.txt
quarto render     # a _site/
quarto preview
```

`.devcontainer/` levanta ese mismo entorno en un Codespace, y lo hace **todo en `post-create.sh`**, nada en la construcción de la imagen: un build que falla manda el Codespace a modo recuperación, que arranca una imagen ajena (Alpine) y sobrescribe el log en el siguiente arranque, mientras que un fallo en `post-create.sh` deja el contenedor en pie y el error a la vista. Por eso no hay *features* ni `Dockerfile`: solo `base:ubuntu-24.04` —el mismo Ubuntu del runner de Actions, con Python 3.12 de serie— y un script reejecutable que instala `build-essential`, `python3-dev` y `libopenblas-dev` para el backend C de PyTensor, el `.deb` de Quarto con la versión fijada en una variable, `uv` desde su release, y el venv con `requirements.txt`. `QUARTO_PYTHON` apunta a ese venv. Es solo para las slides: el taller va por Colab. `requirements.txt` sigue siendo la única lista de dependencias, así que no hay `pyproject.toml` ni `uv.lock` que mantener en paralelo.

El render ejecuta MCMC: la primera vez tarda un rato (unos 45 s en el runner de Actions; en local, lo que dé la máquina). `freeze: auto` guarda resultados en `_freeze/`, que **no se commitea**: el workflow de Pages cachea ese directorio por su cuenta, en el paso `Restore Quarto freeze cache` de `.github/workflows/publish.yml`. Ese paso **no tiene `restore-keys` a propósito**, y tampoco lo necesita: Quarto invalida `_freeze/` por el hash del código de la celda, no por lo que la celda importa, así que un cambio en `src/` no lo toca y una caché restaurada por prefijo publicaría las figuras viejas. Por lo mismo, **si tocas `src/estilo.py` borra `_freeze/` en local** antes de volver a renderizar, o no verás el cambio.

## Al terminar un cambio

- Si tocas el código de una celda, `_freeze/` queda obsoleto para esa celda: vuelve a renderizar para comprobar que sigue saliendo lo que esperas. `_freeze/` se queda en local.
- Si tocas `notebooks/taller.ipynb` —un enunciado, una celda, el orden de las secciones—, replícalo en `notebooks/taller-solucion.ipynb`. Los dos notebooks se editan a la vez o se desincronizan en una sesión.
- Si añades dependencias, actualiza `requirements.txt`.
- Si cambias la estructura, actualiza `README.md` y este fichero.
