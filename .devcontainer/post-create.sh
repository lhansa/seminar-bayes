#!/usr/bin/env bash
# Monta el entorno de las slides al crear el Codespace: compilador, Quarto, uv y
# el venv con requirements.txt.
#
# Todo pasa aquí y nada en la construcción de la imagen, a propósito. Lo que falla
# durante el build manda el Codespace a modo recuperación, que arranca una imagen
# ajena y se lleva el log por delante en el siguiente arranque. Lo que falla aquí
# deja el contenedor en pie, escribe el error en el terminal y se puede volver a
# lanzar con `bash .devcontainer/post-create.sh` sin reconstruir nada.
#
# El script es reejecutable: se puede lanzar dos veces seguidas sin romper nada.
set -euo pipefail

# Versión fijada a mano. Las series pares de Quarto son el canal estable; las
# impares, la pre-release. Para actualizar, esta línea y nada más.
QUARTO_VERSION="1.10.18"

echo "==> Paquetes de sistema"
# build-essential y python3-dev son para el backend C de PyTensor, que compila
# contra Python.h cada vez que se ajusta un modelo. libopenblas-dev es lo mismo
# que instala .github/workflows/publish.yml.
# Un repo de terceros caído no debe tumbar el script: el que manda es el install.
sudo apt-get update -qq || echo "(aviso: apt-get update dio error; se intenta instalar igualmente)"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential libopenblas-dev python3 python3-dev curl ca-certificates

echo "==> Quarto ${QUARTO_VERSION}"
if [ "$(quarto --version 2>/dev/null || true)" != "${QUARTO_VERSION}" ]; then
    tmp="$(mktemp -d)"
    curl -fsSL -o "${tmp}/quarto.deb" \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb"
    # apt install en vez de dpkg -i: resuelve las dependencias del paquete.
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${tmp}/quarto.deb"
    rm -rf "${tmp}"
fi

echo "==> uv"
if ! command -v uv >/dev/null 2>&1; then
    tmp="$(mktemp -d)"
    curl -fsSL -o "${tmp}/uv.tar.gz" \
        "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz"
    sudo tar -xzf "${tmp}/uv.tar.gz" --strip-components 1 -C /usr/local/bin
    rm -rf "${tmp}"
fi

echo "==> Entorno de Python"
uv venv --python 3.12 --seed .venv
uv pip install --python .venv/bin/python -r requirements.txt

# Que los terminales nuevos arranquen con el venv activado. Quarto no lo necesita:
# usa el intérprete de QUARTO_PYTHON, que devcontainer.json deja apuntando al venv.
ACTIVAR="source \"${PWD}/.venv/bin/activate\""
grep -qxF "${ACTIVAR}" "${HOME}/.bashrc" || echo "${ACTIVAR}" >> "${HOME}/.bashrc"

echo "==> Comprobación"
quarto --version
.venv/bin/python -c "import pymc, arviz; print('pymc', pymc.__version__, '| arviz', arviz.__version__)"
echo "Entorno listo. quarto render para generar _site/."
