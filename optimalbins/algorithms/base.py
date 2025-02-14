from abc import ABC, abstractmethod
from typing import List, Dict, Any
from optimalbins.models.item import Item
from optimalbins.models.bin import Bin
from optimalbins.common.packing_result import PackingResult

class BaseBinPacking(ABC):
    @abstractmethod
    def pack(self, items: List[Item], bins: List[Bin], **kwargs: Any) -> PackingResult:
        """
        Ejecuta el algoritmo de empaquetado.

        :param items: Lista de objetos Item a empaquetar.
        :param bins: Lista de objetos Bin donde se intentará colocar los items.
        :param kwargs: Parámetros adicionales de configuración.
        :return: Una instancia de PackingResult que contiene los bins actualizados y métricas del proceso.
        """
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """
        Devuelve las métricas del proceso de empaquetado, como tiempo de ejecución, porcentaje de utilización, etc.

        :return: Un diccionario con las métricas obtenidas.
        """
        pass
