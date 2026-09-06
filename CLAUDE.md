# CLAUDE.md

Instrucciones para agentes que trabajen en este repositorio.

## Qué es esto

Material de un seminario sobre inferencia bayesiana, en dos partes:

- **Parte 1 (~1 h):** slides revealjs en `index.qmd`.
- **Parte 2 (~1 h):** taller práctico en `notebooks/taller.ipynb`, con otro conjunto de datos (pendiente de decidir).

Público: profesionales de datos. Saben Python y regresión; no saben bayesiana. Se puede dar por sabido OLS, p-valores e intervalos de confianza.

Idioma de todo el material: **español**. Los nombres de fichero, variables y ramas, en inglés o español según ya estén; no renombrar por gusto.

## Origen del contenido

El guion de la parte teórica sale de `cartas/01-inferencia-estadistica/carta.qmd` del repositorio **`estadistica-correspondencia`**, del mismo autor. Si hay que ampliar una sección de las slides, la fuente de verdad es esa carta: mismos datos, mismas prioris, mismas conclusiones. No inventes resultados nuevos ni cambies los valores de las prioris sin motivo.

`data/radon.csv` es copia del que hay en ese repositorio.

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
- `_quarto.yml` renderiza **solo** `index.qmd`. El notebook del taller queda fuera del sitio a propósito.

## Comandos

```bash
pip install -r requirements.txt
quarto render     # a _site/
quarto preview
```

El render ejecuta MCMC: la primera vez tarda minutos. `freeze: auto` guarda resultados en `_freeze/`, que conviene commitear para que el workflow de Pages no vuelva a muestrear.

## Al terminar un cambio

- Si tocas el código de una celda, `_freeze/` queda obsoleto para esa celda: vuelve a renderizar y commitea el `_freeze/` actualizado.
- Si añades dependencias, actualiza `requirements.txt`.
- Si cambias la estructura, actualiza `README.md` y este fichero.
