from typing import List, Dict, Any
from algorithms.base import BaseBinPacking
from models.item import Item
from models.bin import Bin
from common.packing_result import PackingResult

class FirstFit2D(BaseBinPacking):
    def pack(self, items: List[Item], bins: List[Bin], **kwargs: Any) -> PackingResult:
        """
        Implementación sencilla del algoritmo First Fit para empaquetado 2D.
        Asigna cada item al primer bin en el que quepa; si ninguno lo contiene, crea un nuevo bin.
        """
        for item in items:
            placed: bool = False
            # Iteramos sobre los bins existentes
            for bin in bins:
                if bin.can_fit(item):
                    bin.add_item(item)
                    placed = True
                    break
            # Si el item no fue colocado, creamos un nuevo bin basado en el primero de la lista
            if not placed:
                if len(bins) == 0:
                    raise ValueError("No hay bins iniciales definidos para crear uno nuevo.")
                base_bin: Bin = bins[0]
                new_bin: Bin = type(base_bin)(
                    id=f"bin_{len(bins)+1}",
                    width=base_bin.width,
                    height=base_bin.height,
                    depth=base_bin.depth
                )
                new_bin.add_item(item)
                bins.append(new_bin)
        return PackingResult(bins=bins, metrics=self.get_metrics())

    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas de ejemplo para el algoritmo FirstFit2D.
        En una implementación real se incluirían datos como tiempo de ejecución,
        porcentaje de utilización del espacio, etc.
        """
        return {"algorithm": "FirstFit2D", "description": "Métricas de ejemplo"}
