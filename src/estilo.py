"""Estilo común de matplotlib para las slides y el notebook del taller.

Un único punto donde se define el aspecto de todas las figuras, para que las
slides de la parte teórica y el notebook del taller se vean igual.

Uso:

    from src.estilo import aplicar_estilo
    aplicar_estilo()
"""

from cycler import cycler
import matplotlib.pyplot as plt

# Morado del tema de las slides (custom.scss), para acentos puntuales
ACENTO = "#800080"

# Escala de grises para series múltiples
GRISES = ["#000000", "#4A4A4A", "#7A7A7A", "#AAAAAA"]


def aplicar_estilo():
    """Aplica el estilo del seminario a matplotlib."""
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.labelcolor": "black",
            "text.color": "black",
            "xtick.color": "black",
            "ytick.color": "black",
            "grid.color": "#CCCCCC",
            "grid.linestyle": "--",
            "grid.linewidth": 0.5,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "axes.prop_cycle": cycler("color", GRISES),
            "figure.dpi": 110,
            "savefig.dpi": 140,
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
            "font.size": 13,
            "axes.titlesize": 13,
            "axes.labelsize": 13,
            "legend.fontsize": 12,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
        }
    )
