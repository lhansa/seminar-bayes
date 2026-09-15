#!/usr/bin/env bash
# Monta el entorno de las slides al crear el Codespace: venv con uv y las
# dependencias de requirements.txt. Quarto usa ese intérprete vía QUARTO_PYTHON
# (definido en devcontainer.json), esté o no activado el venv en la shell.
set -euo pipefail

uv venv --python 3.12 --seed .venv
uv pip install --python .venv/bin/python -r requirements.txt

# Que los terminales nuevos arranquen con el venv activado.
ACTIVAR="source \"${PWD}/.venv/bin/activate\""
grep -qxF "${ACTIVAR}" "${HOME}/.bashrc" || echo "${ACTIVAR}" >> "${HOME}/.bashrc"

echo "Entorno listo. quarto render para generar _site/."
