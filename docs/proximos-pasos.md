# Próximos pasos

Propuesta de issues para abrir en el repositorio. Cada sección es un issue: título en el encabezado y cuerpo debajo.

---

## 1. Elegir el conjunto de datos del taller (parte 2)

Bloquea el resto del trabajo sobre `notebooks/taller.ipynb`, que ahora mismo se apoya en `data/radon.csv` como placeholder.

Requisitos del conjunto (están también en `data/README.md`):

- variable respuesta continua, o transformable con un logaritmo;
- al menos un predictor a nivel de observación;
- variable de grupo con **muchos grupos y número de observaciones muy desigual entre ellos** — sin ese desequilibrio el modelo jerárquico no luce;
- licencia que permita redistribuirlo en este repositorio;
- tamaño razonable: el MCMC tiene que terminar en minutos.

Conviene además que el dominio le suene a un profesional de datos (ventas por tienda, conversión por campaña, tiempos por centro) para que la última sección del taller —la pregunta concreta que responde la posteriori— tenga sentido de negocio.

**Etiquetas sugeridas:** `taller`, `bloqueante`

---

## 2. Rellenar el notebook del taller con el dataset elegido

Depende del issue 1.

- Sustituir la celda de carga y las constantes `RESPUESTA`, `PREDICTOR`, `GRUPO`, `GRUPO_CODIGO`.
- Revisar que las prioris siguen justificadas por la escala de la nueva variable. Es el punto donde más fácil se cuela un número heredado del radón.
- Comprobar que el modelo jerárquico converge sin divergencias con `target_accept=0.95`.

**Etiquetas sugeridas:** `taller`

---

## 3. Escribir la versión resuelta del taller

Un `notebooks/taller-solucion.ipynb` con los ocho ejercicios resueltos, para tenerlo delante durante la sesión y poder publicarlo después.

Decidir si se publica junto a las slides o se entrega aparte al terminar.

**Etiquetas sugeridas:** `taller`

---

## 4. Activar GitHub Pages y verificar el primer despliegue

En *Settings → Pages*, poner **GitHub Actions** como origen. Después, lanzar el workflow a mano (`workflow_dispatch`) y comprobar:

- que `pymc` compila en el runner (por eso el workflow instala `gcc`, `g++` y `libopenblas-dev`);
- cuánto tarda el render completo con MCMC, para saber si merece la pena commitear `_freeze/`;
- que las slides se ven bien en la URL publicada, sobre todo las tablas y el gráfico de shrinkage.

**Etiquetas sugeridas:** `infra`

---

## 5. Renderizar en local y commitear `_freeze/`

Depende del issue 4, o al menos de haber medido el tiempo de render.

Con `freeze: auto`, si `_freeze/` está en el repositorio el workflow no vuelve a muestrear y el despliegue baja de minutos a segundos. El coste es acordarse de regenerarlo cada vez que cambie el código de una celda.

**Etiquetas sugeridas:** `infra`

---

## 6. Cronometrar la parte teórica y ajustarla a una hora

El draft actual tiene unas 45 slides. Muchas son de una línea, así que la cuenta engaña.

Sospechas de por dónde recortar si sobra:

- la comprobación predictiva previa se puede contar sin el gráfico de dos paneles;
- el modelo unpooled se puede reducir a una slide, ya que solo existe para justificar el jerárquico;
- la tabla de predicción por vivienda es densa: o se explica despacio o se quita.

Y si falta material: el diagnóstico del muestreador (traza, `r_hat`, ESS, divergencias) está en la carta y no ha entrado aquí.

**Etiquetas sugeridas:** `slides`

---

## 7. Añadir notas del ponente a las slides que las necesiten

Solo la slide de la comprobación predictiva previa tiene `::: {.notes}`. Las que más lo piden:

- la apertura de Obama, para no alargarse;
- "He dado la vuelta al problema", que es el giro del bloque de la moneda;
- el gráfico de shrinkage, con las cifras del cociente de varianzas a mano.

**Etiquetas sugeridas:** `slides`

---

## 8. Decidir qué se hace con la parametrización no centrada

El modelo jerárquico va con parametrización centrada, como en la carta. Si aparecen divergencias al renderizar, hay que decidir entre:

- dejarlas y explicarlas como lo que son (una dificultad geométrica del muestreador, no del fenómeno), que es lo que hace la carta;
- añadir una slide con la reparametrización $\alpha_c = \mu_\alpha + \sigma_\alpha z_c$;
- reparametrizar sin contarlo, que es la opción mala.

**Etiquetas sugeridas:** `slides`, `contenido`

---

## 9. Slide de requisitos previos para el taller

Antes de la sesión hace falta que la gente llegue con el entorno montado: Python 3.12, `pip install -r requirements.txt` y `gcc`/`g++` para el backend de PyTensor, que en Windows es donde da guerra.

Decidir si esto va en una slide al final de la parte teórica, en un correo previo, o en las dos.

**Etiquetas sugeridas:** `slides`, `taller`

---

## 10. Actualizar el QR y el material de captación

`img/qr.png` viene copiado de `ceu-2606`. Comprobar a dónde apunta y, si toca, regenerarlo hacia una página de leonardohansa.com específica del seminario.

**Etiquetas sugeridas:** `marketing`
