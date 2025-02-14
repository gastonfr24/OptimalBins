import unittest
import matplotlib.pyplot as plt
from optimalbins.models.item import Item
from optimalbins.models.bin import Bin
from optimalbins.algorithms._2d.guillotine import Guillotine2D
from optimalbins.common.packing_result import PackingResult

class TestGuillotineHeuristics(unittest.TestCase):
    def setUp(self):
        """ Configuración inicial del test con bins y items de prueba """
        self.bins = [Bin(f"bin_{i}", width=10, height=10) for i in range(4)]
        self.items = [
            Item("A", width=4, height=4),
            Item("B", width=3, height=6),
            Item("C", width=2, height=2),
            Item("D", width=5, height=3),
            Item("E", width=3, height=3),
        ]
        self.heuristics = ["default", "alternative", "shorter_side", "longer_side"]

    def test_heuristics(self):
        """ Prueba las distintas heurísticas del algoritmo Guillotine2D y visualiza los resultados """
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        axes = axes.flatten()

        for i, heuristic in enumerate(self.heuristics):
            bins = [Bin(f"bin_{i}", width=10, height=10) for i in range(1)]
            guillotine = Guillotine2D(heuristic=heuristic)
            result: PackingResult = guillotine.pack(self.items, bins)

            # Generar gráfico de la disposición de los ítems
            ax = axes[i]
            ax.set_title(f"Heurística: {heuristic}")
            self.plot_packing(ax, bins[0])

        plt.tight_layout()
        plt.show()

    def plot_packing(self, ax, bin):
        """ Genera la visualización del bin con los ítems colocados """
        ax.set_xlim(0, bin.width)
        ax.set_ylim(0, bin.height)
        ax.set_xticks(range(bin.width + 1))
        ax.set_yticks(range(bin.height + 1))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        for item in bin.items:
            rect = plt.Rectangle((item.x, item.y), item.width, item.height, 
                                 edgecolor="black", facecolor="lightblue", alpha=0.7)
            ax.add_patch(rect)
            ax.text(item.x + item.width / 2, item.y + item.height / 2, item.id, 
                    ha='center', va='center', fontsize=10, color="black")

if __name__ == "__main__":
    unittest.main()
