from typing import List
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from optimalbins.models.bin import Bin

def plot_bins(bins: List[Bin], show_free_rectangles: bool = True) -> None:
    """
    Genera gráficos para cada bin en la lista.
    Se basa en la lógica de visualización de PackingResult.plot().
    
    Si show_free_rectangles es True y el bin tiene el atributo 'free_rectangles',
    se dibujarán estos rectángulos (áreas libres) en color rojo con línea discontinua.
    """
    for bin in bins:
        fig, ax = plt.subplots()
        ax.set_title(f"Bin {bin.id}")
        # Dibujar el contorno del bin
        bin_rect = Rectangle((0, 0), bin.width, bin.height, fill=None, edgecolor="black", linewidth=2)
        ax.add_patch(bin_rect)
        # Dibujar cada ítem (se asume que cada ítem tiene atributos 'x' e 'y')
        for item in bin.items:
            x = getattr(item, 'x', 0)
            y = getattr(item, 'y', 0)
            item_rect = Rectangle((x, y), item.width, item.height, fill=True, edgecolor="blue", alpha=0.5)
            ax.add_patch(item_rect)
            ax.text(x + item.width / 2, y + item.height / 2, str(item.id), 
                    ha="center", va="center", fontsize=8, color="white")
        # Dibujar los rectángulos libres si el parámetro está activo y el bin tiene ese atributo.
        if show_free_rectangles and hasattr(bin, "free_rectangles"):
            for free_rect in bin.free_rectangles:
                fx, fy, fwidth, fheight = free_rect
                free_patch = Rectangle((fx, fy), fwidth, fheight, fill=False,
                                       edgecolor="red", linestyle="--", linewidth=1.5)
                ax.add_patch(free_patch)
        ax.set_xlim(0, bin.width)
        ax.set_ylim(0, bin.height)
        ax.set_xlabel("Ancho")
        ax.set_ylabel("Alto")
        plt.show()
