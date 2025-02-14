from typing import List, Tuple, Optional, Dict, Any
from algorithms.base import BaseBinPacking
from models.item import Item
from models.bin import Bin
from common.packing_result import PackingResult

class BottomLeft2D(BaseBinPacking):
    def pack(self, items: List[Item], bins: List[Bin], **kwargs: Any) -> PackingResult:
        """
        Implementación del algoritmo Bottom-Left para empaquetado 2D.
        Para cada item, se buscan posiciones candidatas en cada bin en que quepa sin solaparse.
        Si no es posible colocar el item en los bins existentes, se crea un nuevo bin (basado en el primero).
        """
        for item in items:
            placed: bool = False
            # Intentamos colocar el item en alguno de los bins existentes.
            for bin in bins:
                candidate: Optional[Tuple[float, float]] = self.find_position(bin, item)
                if candidate is not None:
                    x, y = candidate
                    item.set_position(x, y)
                    bin.add_item(item)
                    placed = True
                    break
            if not placed:
                # Si no se pudo colocar el item, se crea un nuevo bin basado en el primero.
                if not bins:
                    raise ValueError("No hay un bin base definido para crear uno nuevo.")
                base_bin: Bin = bins[0]
                new_bin: Bin = type(base_bin)(
                    id=f"bin_{len(bins) + 1}",
                    width=base_bin.width,
                    height=base_bin.height,
                    depth=base_bin.depth
                )
                # En un bin nuevo (vacío), el item se coloca en (0,0)
                candidate = (0.0, 0.0)
                item.set_position(*candidate)
                new_bin.add_item(item)
                bins.append(new_bin)
        return PackingResult(bins=bins, metrics=self.get_metrics())

    def find_position(self, bin: Bin, item: Item) -> Optional[Tuple[float, float]]:
        """
        Calcula la mejor posición para ubicar 'item' en 'bin' usando el criterio Bottom-Left.
        Se generan posiciones candidatas a partir de (0,0) y de los bordes de los items ya colocados.
        Se retorna la posición (x,y) válida con menor y y, en caso de empate, con menor x.
        """
        # Posición inicial (0,0) siempre es candidata.
        candidate_positions: List[Tuple[float, float]] = [(0.0, 0.0)]
        
        # Genera candidatos basados en los items ya colocados.
        for placed in bin.items:
            # Posición a la derecha del item colocado.
            candidate_positions.append((placed.x + placed.width, placed.y))
            # Posición sobre el item colocado.
            candidate_positions.append((placed.x, placed.y + placed.height))
        
        # Filtra posiciones que cumplan:
        #   - El item, colocado en esa posición, debe estar dentro de los límites del bin.
        #   - No debe solaparse con ningún item ya colocado.
        valid_candidates: List[Tuple[float, float]] = []
        for (cx, cy) in candidate_positions:
            if cx + item.width <= bin.width and cy + item.height <= bin.height:
                if not self.overlap(bin, item, cx, cy):
                    valid_candidates.append((cx, cy))
        
        if not valid_candidates:
            return None
        
        # Selecciona el candidato con el menor valor de y y, en caso de empate, el de menor x.
        valid_candidates.sort(key=lambda pos: (pos[1], pos[0]))
        return valid_candidates[0]

    def overlap(self, bin: Bin, item: Item, x: float, y: float) -> bool:
        """
        Verifica si ubicar 'item' en la posición (x,y) en 'bin' solaparía con algún item ya colocado.
        """
        for placed in bin.items:
            if self.rectangles_overlap(x, y, item.width, item.height,
                                        placed.x, placed.y, placed.width, placed.height):
                return True
        return False

    def rectangles_overlap(
        self,
        x1: float, y1: float, w1: float, h1: float,
        x2: float, y2: float, w2: float, h2: float
    ) -> bool:
        """
        Determina si dos rectángulos se solapan.
        Los rectángulos se definen por su esquina inferior izquierda (x,y), ancho y alto.
        """
        # No se solapan si uno está completamente a la derecha, a la izquierda, arriba o abajo del otro.
        if x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1:
            return False
        return True

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas de ejemplo para este algoritmo.
        """
        return {"algorithm": "BottomLeft2D", "description": "Posicionamiento Bottom-Left para evitar solapamientos."}
