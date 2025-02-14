# File: tests/test_maxrect2d.py

import unittest
import matplotlib
# Configuramos un backend no interactivo para los tests (esto evita que plt.show() bloquee la ejecución)
# matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optimalbins.models.item import Item
from optimalbins.models.bin import Bin
from optimalbins.algorithms._2d.maxrects import MaxRects2D
from optimalbins.common.packing_result import PackingResult

class TestMaxRects2D(unittest.TestCase):
    def setUp(self) -> None:
        # Definimos un bin de 10x10 para las pruebas
        self.bin_width = 10
        self.bin_height = 10
        
        # Definimos un conjunto de ítems de prueba
        self.base_items = [
            Item("A", 3, 3),
            Item("B", 4, 2),
            Item("C", 2, 2),
            Item("D", 5, 3),
            Item("E", 3, 4)
        ]
        
        # Definimos las heurísticas a probar, usando guiones bajos
        self.heuristics = [
            "best_short_side_fit",
            "best_long_side_fit",
            "best_area_fit",
            "bottom_left",
            "contact_point_rule"
        ]
    
    def test_maxrects_heuristics_visualization(self) -> None:
        """
        Prueba el algoritmo MaxRects2D con distintas heurísticas y visualiza el resultado.
        Se crea un subplot para cada heurística mostrando la distribución de los ítems en el bin.
        """
        # Creamos una figura con un subplot para cada heurística
        num_heuristics = len(self.heuristics)
        # Para disponer en una cuadrícula (por ejemplo, 2 filas)
        rows = (num_heuristics + 2 - 1) // 2
        cols = 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*5))
        # Aplanamos la lista de ejes para iterar fácilmente (en caso de que solo haya 1 fila, axes es un array 1D)
        if rows * cols > 1:
            axes = axes.flatten()
        else:
            axes = [axes]
        
        # Iteramos sobre las heurísticas
        for i, heuristic in enumerate(self.heuristics):
            # Para cada heurística, creamos un nuevo bin y una copia fresca de los ítems.
            test_bin = Bin("bin_test", width=self.bin_width, height=self.bin_height)
            # Se instancian nuevos ítems (para evitar interferencia entre pruebas)
            items = [
                Item("A", 3, 3),
                Item("B", 4, 2),
                Item("C", 2, 2),
                Item("D", 5, 3),
                Item("E", 3, 4)
            ]
            # Instanciamos el algoritmo MaxRects2D con la heurística actual.
            algorithm = MaxRects2D(heuristic=heuristic)
            result: PackingResult = algorithm.pack(items, [test_bin])
            
            ax = axes[i]
            ax.set_title(f"Heurística: {heuristic}")
            ax.set_xlim(0, test_bin.width)
            ax.set_ylim(0, test_bin.height)
            ax.set_xticks(range(test_bin.width+1))
            ax.set_yticks(range(test_bin.height+1))
            ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            
            # Dibujamos cada ítem en el bin.
            for item in test_bin.items:
                rect = plt.Rectangle(
                    (item.x, item.y), item.width, item.height,
                    edgecolor="black", facecolor="lightgreen", alpha=0.7
                )
                ax.add_patch(rect)
                # Usamos item.id para etiquetar
                ax.text(
                    item.x + item.width / 2,
                    item.y + item.height / 2,
                    item.id,
                    ha="center", va="center", fontsize=10, color="black"
                )
        
        # En caso de que queden subplots sin usar, los ocultamos.
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")
        
        plt.tight_layout()
        # Mostrar el gráfico (en un entorno interactivo se visualizará la figura)
        plt.show()

if __name__ == "__main__":
    unittest.main()
