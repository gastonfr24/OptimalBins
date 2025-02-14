from typing import List, Tuple, Dict, Any, Optional
from optimalbins.algorithms.base import BaseBinPacking
from optimalbins.models.item import Item
from optimalbins.models.bin import Bin
from optimalbins.common.packing_result import PackingResult

# Tipo para un rectángulo: (x, y, width, height)
Rect = Tuple[float, float, float, float]

class MaxRects2D(BaseBinPacking):
    def __init__(self, heuristic: str = "best_short_side_fit") -> None:
        """
        Inicializa el algoritmo MaxRects para empaquetado 2D.
        
        :param heuristic: Estrategia de colocación a usar. Valores posibles:
                          "best_short_side_fit", "best_long_side_fit", "best_area_fit",
                          "bottom_left", "contact_point_rule".
        """
        self.heuristic = heuristic

    def pack(self, items: List[Item], bins: List[Bin], **kwargs: Any) -> PackingResult:
        """
        Ejecuta el algoritmo MaxRects para empaquetado 2D.
        
        Para cada bin:
          - Se inicializa la lista de rectángulos libres con el área completa del bin.
          - Para cada ítem (idealmente, se podría ordenar los ítems de mayor a menor área),
            se busca la mejor posición en base a la heurística seleccionada.
          - Si se encuentra una posición, se coloca el ítem y se actualiza la lista
            de rectángulos libres dividiendo TODOS los free rectangles que intersecten
            con el área ocupada por el ítem, y luego se poda la lista.
        
        :return: Un PackingResult con los bins actualizados y las métricas.
        """
        for bin in bins:
            # Inicializamos el espacio libre con el área completa del bin.
            free_rectangles: List[Rect] = [(0.0, 0.0, bin.width, bin.height)]
            
            for item in items:
                # Buscamos la mejor posición en la lista actual de free rectangles.
                best_pos = self.find_best_position(free_rectangles, item)
                if best_pos is not None:
                    x, y, best_rect_index = best_pos
                    # Colocamos el ítem en esa posición.
                    item.set_position(x, y)
                    bin.add_item(item)
                    # Definimos el rectángulo ocupado por el ítem.
                    placed_rect: Rect = (x, y, item.width, item.height)
                    # Actualizamos la lista de free rectangles:
                    free_rectangles = self.update_free_rectangles(free_rectangles, placed_rect)
                else:
                    # Si el ítem no cabe en este bin, se omite para este bin (o se intentaría en otro).
                    pass
            
            # Opcional: se puede aplicar una poda final.
            free_rectangles = self.prune_free_rectangles(free_rectangles)
            # Si deseas que el bin guarde la lista de free rectangles para visualización, la asignamos.
            bin.free_rectangles = free_rectangles  # Esto es opcional y se usará en el plot.
        
        return PackingResult(bins=bins, metrics=self.get_metrics())
    
    def find_best_position(
        self,
        free_rectangles: List[Rect],
        item: Item
    ) -> Optional[Tuple[float, float, int]]:
        """
        Recorre todos los rectángulos libres y retorna la mejor posición (x, y, index)
        para colocar el ítem, de acuerdo con la heurística seleccionada.
        """
        best_score: Optional[float] = None
        best_position: Optional[Tuple[float, float]] = None
        best_index: int = -1
        
        for idx, (rx, ry, rwidth, rheight) in enumerate(free_rectangles):
            if item.width <= rwidth and item.height <= rheight:
                score = self.evaluate_position(rx, ry, rwidth, rheight, item)
                if best_score is None or score < best_score:
                    best_score = score
                    best_position = (rx, ry)
                    best_index = idx
        if best_position is not None:
            return (best_position[0], best_position[1], best_index)
        return None
    
    def evaluate_position(
        self,
        rx: float, ry: float, rwidth: float, rheight: float,
        item: Item
    ) -> float:
        """
        Evalúa la calidad de colocar el ítem en el rectángulo libre (rx, ry, rwidth, rheight)
        según la heurística seleccionada.
        """
        leftover_horiz = rwidth - item.width
        leftover_vert = rheight - item.height
        key = self.heuristic.lower()
        
        if key == "best_short_side_fit":
            return min(leftover_horiz, leftover_vert)
        elif key == "best_long_side_fit":
            return max(leftover_horiz, leftover_vert)
        elif key == "best_area_fit":
            return (rwidth * rheight) - (item.width * item.height)
        elif key == "bottom_left":
            return ry * 10000 + rx
        elif key == "contact_point_rule":
            contact_score = self.calculate_contact_score(rx, ry, rwidth, rheight, item)
            return -contact_score
        else:
            return min(leftover_horiz, leftover_vert)
    
    def calculate_contact_score(
        self,
        rx: float, ry: float, rwidth: float, rheight: float,
        item: Item
    ) -> float:
        """
        Calcula un "contact score" para el ítem en el rectángulo libre.
        Aquí se utiliza una función simple: la suma de los lados del rectángulo libre.
        """
        return rwidth + rheight

    def update_free_rectangles(
        self,
        free_rectangles: List[Rect],
        placed_rect: Rect
    ) -> List[Rect]:
        """
        Dado un conjunto de free rectangles y el rectángulo ocupado (placed_rect),
        actualiza la lista dividiendo cada free rectangle que intersecte con el placed_rect.
        """
        updated_rectangles: List[Rect] = []
        for fr in free_rectangles:
            if self.rectangles_intersect(fr, placed_rect):
                split_rects = self.split_free_rectangle(fr, placed_rect)
                updated_rectangles.extend(split_rects)
            else:
                updated_rectangles.append(fr)
        return self.prune_free_rectangles(updated_rectangles)
    
    def rectangles_intersect(self, fr: Rect, pr: Rect) -> bool:
        """
        Determina si el free rectangle (fr) y el placed rectangle (pr) se intersectan.
        """
        fx, fy, fw, fh = fr
        px, py, pw, ph = pr
        return not (fx >= px + pw or fx + fw <= px or fy >= py + ph or fy + fh <= py)
    
    def split_free_rectangle(self, fr: Rect, pr: Rect) -> List[Rect]:
        """
        Divide el free rectangle 'fr' con respecto al placed rectangle 'pr'.
        Se generan hasta 4 nuevos rectángulos resultantes del área no ocupada por pr.
        """
        fx, fy, fw, fh = fr
        px, py, pw, ph = pr
        new_rects: List[Rect] = []
        
        # Si hay una sección por encima del placed rect.
        if py + ph < fy + fh:
            new_rects.append((fx, py + ph, fw, (fy + fh) - (py + ph)))
        
        # Si hay una sección por debajo del placed rect.
        if py > fy:
            new_rects.append((fx, fy, fw, py - fy))
        
        # Si hay una sección a la izquierda del placed rect.
        if px > fx:
            # Limitar verticalmente al área que no ha sido cortada por arriba o abajo.
            new_rects.append((fx, fy, px - fx, fh))
        
        # Si hay una sección a la derecha del placed rect.
        if px + pw < fx + fw:
            new_rects.append((px + pw, fy, (fx + fw) - (px + pw), fh))
        
        # Filtrar rectángulos con dimensiones negativas o cero.
        valid_rects = [r for r in new_rects if r[2] > 0 and r[3] > 0]
        return valid_rects

    def prune_free_rectangles(self, free_rectangles: List[Rect]) -> List[Rect]:
        """
        Elimina de la lista aquellos free rectangles que están completamente contenidos
        en otro free rectangle.
        """
        pruned: List[Rect] = []
        for i, rect in enumerate(free_rectangles):
            contained = False
            fx, fy, fw, fh = rect
            for j, other in enumerate(free_rectangles):
                if i == j:
                    continue
                ox, oy, ow, oh = other
                if fx >= ox and fy >= oy and (fx + fw) <= (ox + ow) and (fy + fh) <= (oy + oh):
                    contained = True
                    break
            if not contained:
                pruned.append(rect)
        return pruned
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas de ejemplo para el algoritmo MaxRects2D, incluyendo la heurística utilizada.
        """
        return {
            "algorithm": "MaxRects2D",
            "heuristic": self.heuristic,
            "description": "Algoritmo MaxRects para empaquetado 2D con actualización global de free rectangles."
        }
