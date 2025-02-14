import matplotlib.pyplot as plt
# Opcional: usa un backend interactivo (por ejemplo, TkAgg)
plt.switch_backend('TkAgg')

from models.item import Item
from models.bin import Bin
from models.manager import BinManager
from algorithms._2d.bottom_left import BottomLeft2D
from config import VERBOSE, DEFAULT_DIMENSION

def main():
    # Crear algunos items de ejemplo
    items = [
        Item(id="A", width=2, height=3),
        Item(id="B", width=3, height=2),
        Item(id="C", width=1, height=1)
    ]

    # Crear un bin base para 2D (por ejemplo, un contenedor de 5x5)
    base_bin = Bin(id="bin_1", width=5, height=5)

    # Instanciar el algoritmo BottomLeft2D
    algorithm = BottomLeft2D()

    # Crear un BinManager y configurarlo con el algoritmo y la dimensión
    manager = BinManager(dimension=DEFAULT_DIMENSION, algorithm=algorithm)
    manager.add_bin(base_bin)
    
    # Agregar los items al manager
    for item in items:
        manager.add_item(item)
    
    # Ejecutar el empaquetado
    manager.pack()

    # Visualizar el resultado
    manager.plot()

    # Imprimir reporte en consola
    print(manager.report(verbose=VERBOSE))

if __name__ == "__main__":
    main()