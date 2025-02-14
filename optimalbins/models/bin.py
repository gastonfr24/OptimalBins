from typing import Optional, List
from optimalbins.models.item import Item

class Bin:
    def __init__(
        self,
        id: str,
        width: float,
        height: float,
        depth: Optional[float] = None
    ) -> None:
        """
        Inicializa un contenedor (bin) para empaquetado.

        :param id: Identificador único del bin.
        :param width: Ancho del bin.
        :param height: Alto del bin.
        :param depth: Profundidad del bin (si es None, se asume 2D).
        """
        self.id: str = id
        self.width: float = width
        self.height: float = height
        self.depth: Optional[float] = depth
        self.items: List[Item] = []  # Lista de ítems ubicados en este bin

    def can_fit(self, item: Item) -> bool:
        """
        Verifica de forma básica si el item cabe en el bin según sus dimensiones.
        Para 3D se requiere que el item tenga depth y que sus dimensiones sean
        menores o iguales a las del bin.
        """
        if self.depth is not None:
            # Si el bin es 3D, asegurarse de que el ítem tenga profundidad
            if item.depth is None:
                return False
            return (
                item.width <= self.width and 
                item.height <= self.height and 
                item.depth <= self.depth
            )
        else:
            return item.width <= self.width and item.height <= self.height

    def add_item(self, item: Item) -> bool:
        """
        Intenta añadir el item al bin. Si cabe, se agrega a la lista y retorna True;
        de lo contrario retorna False.
        """
        if self.can_fit(item):
            self.items.append(item)
            # Aquí se podría actualizar la estructura interna del espacio libre
            return True
        return False

    def __repr__(self) -> str:
        if self.depth is not None:
            return f"Bin({self.id}, {self.width}x{self.height}x{self.depth}, items={len(self.items)})"
        return f"Bin({self.id}, {self.width}x{self.height}, items={len(self.items)})"
