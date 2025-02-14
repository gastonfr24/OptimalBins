from typing import List, Tuple, Dict, Any, Optional
from optimalbins.algorithms.base import BaseBinPacking
from optimalbins.models.item import Item
from optimalbins.models.bin import Bin
from optimalbins.common.packing_result import PackingResult

class Guillotine2D(BaseBinPacking):
    def __init__(self, heuristic: str = "default") -> None:
        """
        :param heuristic: Estrategia a utilizar. Valores admitidos:
                          "default", "alternative", "shorter_side", "longer_side".
        """
        self.heuristic = heuristic

    def pack(self, items: List[Item], bins: List[Bin], **kwargs: Any) -> PackingResult:
        """
        Implementa el algoritmo Guillotine para empaquetado 2D.
        Para cada bin, se inicializa una lista de rectángulos libres (inicialmente, el área completa del bin).
        Luego, para cada ítem se busca un rectángulo libre en el que quepa. Si se encuentra, se coloca el ítem y
        se actualiza la lista de rectángulos libres mediante cortes (según la heurística elegida).
        """
        # Procesamos cada bin por separado.
        for bin in bins:
            free_rectangles: List[Tuple[float, float, float, float]] = [(0.0, 0.0, bin.width, bin.height)]
            
            for item in items:
                pos: Optional[Tuple[float, float, int]] = self.find_position(free_rectangles, item)
                if pos is not None:
                    x, y, rect_index = pos
                    item.set_position(x, y)
                    bin.add_item(item)
                    used_rect = free_rectangles.pop(rect_index)
                    new_rects = self.split_rectangle(used_rect, item, x, y)
                    free_rectangles.extend(new_rects)
                # Si el ítem no encuentra espacio en este bin, se omite para él.
        return PackingResult(bins=bins, metrics=self.get_metrics())

    def find_position(
        self, 
        free_rectangles: List[Tuple[float, float, float, float]], 
        item: Item
    ) -> Optional[Tuple[float, float, int]]:
        """
        Busca un rectángulo libre en el que el ítem pueda caber.
        Retorna (x, y, índice) si se encuentra una posición, o None en caso contrario.
        """
        for idx, (rx, ry, rwidth, rheight) in enumerate(free_rectangles):
            if item.width <= rwidth and item.height <= rheight:
                return (rx, ry, idx)
        return None

    def split_rectangle(
        self, 
        rect: Tuple[float, float, float, float], 
        item: Item, 
        x: float, 
        y: float
    ) -> List[Tuple[float, float, float, float]]:
        """
        Realiza cortes de guillotina en el rectángulo 'rect' al colocar el 'item' en (x, y).
        Se delega la división a la estrategia definida en self.heuristic.
        """
        key = self.heuristic.lower().replace(" ", "").replace("_", "")
        if key == "default":
            return self._split_default(rect, item, x, y)
        elif key == "alternative":
            return self._split_alternative(rect, item, x, y)
        elif key in ["shorterside", "shorter"]:
            return self._split_shorter_side(rect, item, x, y)
        elif key in ["longerside", "longer"]:
            return self._split_longer_side(rect, item, x, y)
        else:
            raise ValueError(f"Heurística desconocida: {self.heuristic}")

    def _split_default(
        self, 
        rect: Tuple[float, float, float, float], 
        item: Item, 
        x: float, 
        y: float
    ) -> List[Tuple[float, float, float, float]]:
        """
        Estrategia por defecto:
          - Genera un rectángulo a la derecha del ítem (con ancho = sobrante y altura = item.height).
          - Genera un rectángulo en la parte superior (con el ancho completo del rectángulo original y altura = sobrante).
        """
        rx, ry, rwidth, rheight = rect
        new_rectangles: List[Tuple[float, float, float, float]] = []
        right_width = (rx + rwidth) - (x + item.width)
        if right_width > 0:
            new_rectangles.append((x + item.width, y, right_width, item.height))
        top_height = (ry + rheight) - (y + item.height)
        if top_height > 0:
            new_rectangles.append((rx, y + item.height, rwidth, top_height))
        return new_rectangles

    def _split_alternative(
        self, 
        rect: Tuple[float, float, float, float], 
        item: Item, 
        x: float, 
        y: float
    ) -> List[Tuple[float, float, float, float]]:
        """
        Estrategia alternativa:
          - Genera un rectángulo horizontal que usa el resto del ancho del rectángulo original y toda su altura.
          - Genera un rectángulo vertical que usa la parte superior con el ancho del ítem y el resto de la altura.
        """
        rx, ry, rwidth, rheight = rect
        new_rectangles: List[Tuple[float, float, float, float]] = []
        horizontal_width = (rx + rwidth) - (x + item.width)
        if horizontal_width > 0:
            new_rectangles.append((x + item.width, y, horizontal_width, rheight))
        vertical_height = (ry + rheight) - (y + item.height)
        if vertical_height > 0:
            new_rectangles.append((rx, y + item.height, item.width, vertical_height))
        return new_rectangles

    def _split_shorter_side(
        self, 
        rect: Tuple[float, float, float, float], 
        item: Item, 
        x: float, 
        y: float
    ) -> List[Tuple[float, float, float, float]]:
        """
        Estrategia "shorter_side":
        Se calcula el sobrante en ambas direcciones y se prioriza el corte en la dirección
        con el sobrante menor.
        """
        rx, ry, rwidth, rheight = rect
        right_leftover = (rx + rwidth) - (x + item.width)
        top_leftover = (ry + rheight) - (y + item.height)
        new_rectangles: List[Tuple[float, float, float, float]] = []
        if right_leftover <= top_leftover:
            # Cortamos verticalmente (derecha) de forma similar a _split_default
            if right_leftover > 0:
                new_rectangles.append((x + item.width, y, right_leftover, item.height))
            if top_leftover > 0:
                new_rectangles.append((rx, y + item.height, rwidth, top_leftover))
        else:
            # Cortamos horizontalmente (superior) de forma similar a _split_default
            if top_leftover > 0:
                new_rectangles.append((rx, y + item.height, rwidth, top_leftover))
            if right_leftover > 0:
                new_rectangles.append((x + item.width, y, right_leftover, rheight))
        return new_rectangles

    def _split_longer_side(
        self, 
        rect: Tuple[float, float, float, float], 
        item: Item, 
        x: float, 
        y: float
    ) -> List[Tuple[float, float, float, float]]:
        """
        Estrategia "longer_side":
        Se calcula el sobrante en ambas direcciones y se prioriza el corte en la dirección
        con el sobrante mayor.
        """
        rx, ry, rwidth, rheight = rect
        right_leftover = (rx + rwidth) - (x + item.width)
        top_leftover = (ry + rheight) - (y + item.height)
        new_rectangles: List[Tuple[float, float, float, float]] = []
        if right_leftover >= top_leftover:
            if right_leftover > 0:
                new_rectangles.append((x + item.width, y, right_leftover, item.height))
            if top_leftover > 0:
                new_rectangles.append((rx, y + item.height, rwidth, top_leftover))
        else:
            if top_leftover > 0:
                new_rectangles.append((rx, y + item.height, rwidth, top_leftover))
            if right_leftover > 0:
                new_rectangles.append((x + item.width, y, right_leftover, rheight))
        return new_rectangles

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas que incluyen la heurística utilizada.
        """
        return {
            "algorithm": "Guillotine2D",
            "heuristic": self.heuristic,
            "description": "Algoritmo Guillotine para empaquetado 2D con selección de heurística."
        }
