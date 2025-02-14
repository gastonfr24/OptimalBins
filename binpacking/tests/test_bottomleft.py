import unittest
from models.item import Item
from models.bin import Bin
from models.manager import BinManager
from algorithms._2d.bottom_left import BottomLeft2D
from config import VERBOSE, DEFAULT_DIMENSION

import matplotlib
# Usamos un backend no interactivo para que plt.show() no bloquee en testing.
# matplotlib.use("Agg")

class TestBinPacking(unittest.TestCase):
    def setUp(self) -> None:
        # Creamos algunos items de ejemplo
        self.items = [
            Item(id="A", width=2, height=3),
            Item(id="B", width=3, height=2),
            Item(id="C", width=1, height=1)
        ]
        # Creamos un bin base para 2D (por ejemplo, un contenedor de 5x5)
        self.base_bin = Bin(id="bin_1", width=5, height=5)
        # Usamos el algoritmo BottomLeft2D, que evita el solapamiento
        self.algorithm = BottomLeft2D()
        # Creamos el BinManager con la dimensión y el algoritmo especificados
        self.manager = BinManager(dimension=DEFAULT_DIMENSION, algorithm=self.algorithm)
        self.manager.add_bin(self.base_bin)
        for item in self.items:
            self.manager.add_item(item)
        # Ejecutamos el empaquetado
        self.manager.pack()

    def test_item_positions_within_bounds(self) -> None:
        """
        Verifica que cada item esté posicionado dentro de los límites de su bin.
        """
        for bin in self.manager.bins:
            for item in bin.items:
                self.assertGreaterEqual(item.x, 0, f"Item {item.id} tiene x < 0")
                self.assertGreaterEqual(item.y, 0, f"Item {item.id} tiene y < 0")
                self.assertLessEqual(item.x + item.width, bin.width, 
                                     f"Item {item.id} excede el ancho del bin")
                self.assertLessEqual(item.y + item.height, bin.height, 
                                     f"Item {item.id} excede la altura del bin")

    def test_no_overlap(self) -> None:
        """
        Comprueba que no se solapen dos items en el mismo bin.
        """
        for bin in self.manager.bins:
            for i in range(len(bin.items)):
                for j in range(i + 1, len(bin.items)):
                    item1 = bin.items[i]
                    item2 = bin.items[j]
                    # Dos rectángulos no se solapan si uno está completamente a la izquierda, a la derecha,
                    # arriba o abajo del otro.
                    overlap = not (
                        item1.x + item1.width <= item2.x or
                        item2.x + item2.width <= item1.x or
                        item1.y + item1.height <= item2.y or
                        item2.y + item2.height <= item1.y
                    )
                    self.assertFalse(overlap, f"Items {item1.id} y {item2.id} se solapan.")

    def test_report(self) -> None:
        """
        Verifica que el reporte generado contenga la información esperada.
        """
        report = self.manager.report(verbose=VERBOSE)
        self.assertIsInstance(report, str)
        self.assertIn("Reporte de Empaquetado", report)
        print("\nReporte de Empaquetado:")
        print(report)

    def test_visualization(self) -> None:
        """
        Comprueba que el método plot() se ejecute sin lanzar excepciones.
        Con el backend "Agg" la figura se genera sin mostrarse.
        """
        try:
            self.manager.plot()
        except Exception as e:
            self.fail(f"El método plot() lanzó una excepción: {e}")

if __name__ == "__main__":
    unittest.main()
