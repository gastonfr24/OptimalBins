from typing import Optional, List, Dict, Any, Literal
from models.item import Item
from models.bin import Bin
from algorithms.base import BaseBinPacking
from common.packing_result import PackingResult

from algorithms._2d.bottom_left import BottomLeft2D

class BinManager:
    def __init__(
        self,
        dimension: str = "2D",
        algorithm: Optional[Literal["bottom_left", "guillotine"]] = "bottom_left",
        config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        :param dimension: "2D" o "3D"
        :param algorithm: Puede ser una instancia de un algoritmo de empaquetado o una cadena.
            Si se pasa "Bottom_Left" (o variantes), se utilizará el algoritmo BottomLeft2D.
            Si se omite, se usará BottomLeft2D por defecto.
        :param config: Diccionario de configuraciones adicionales. Si no se proporciona, se usará el config por defecto.
        """
        self.dimension: str = dimension

        # Determinamos el algoritmo a usar.
        if algorithm is None:
            # Si no se especifica, se usa el algoritmo por defecto.
            self.algorithm: BaseBinPacking = BottomLeft2D()
        elif isinstance(algorithm, str):
            # Convertimos la cadena a minúsculas y quitamos espacios y guiones bajos.
            algo_key = algorithm.lower().replace("_", "").replace(" ", "")
            if algo_key == "bottomleft":
                self.algorithm = BottomLeft2D()
            else:
                raise ValueError(f"Algoritmo desconocido: {algorithm}")
        else:
            # Si se pasa una instancia, la usamos directamente.
            self.algorithm = algorithm

        # Configuración global: si no se pasa config, se usa la siguiente por defecto.
        self.config: Dict[str, Any] = config if config is not None else {"default_algorithm": "Bottom_Left"}

        self.bins: List[Bin] = []    # Lista de bins a utilizar
        self.items: List[Item] = []  # Lista de items a empaquetar
        self.result: Optional[PackingResult] = None

    def set_algorithm(self, algorithm: Any) -> None:
        """
        Permite cambiar el algoritmo de empaquetado. Se acepta una instancia o una cadena.
        """
        if isinstance(algorithm, str):
            algo_key = algorithm.lower().replace("_", "").replace(" ", "")
            if algo_key == "bottomleft":
                self.algorithm = BottomLeft2D()
            else:
                raise ValueError(f"Algoritmo desconocido: {algorithm}")
        else:
            self.algorithm = algorithm

    def add_bin(self, bin_instance: Bin) -> None:
        self.bins.append(bin_instance)

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def pack(self) -> PackingResult:
        """
        Ejecuta el algoritmo de empaquetado y guarda el resultado.
        :raises ValueError: Si no se ha definido un algoritmo de empaquetado.
        :return: Instancia de PackingResult con los bins actualizados y métricas del proceso.
        """
        if self.algorithm is None:
            raise ValueError("No se ha definido un algoritmo de empaquetado.")
        self.result = self.algorithm.pack(self.items, self.bins, **self.config)
        return self.result

    def plot(self) -> None:
        """
        Invoca la visualización del resultado mediante el método plot() de PackingResult.
        :raises ValueError: Si pack() no se ha ejecutado previamente.
        """
        if self.result is None:
            raise ValueError("Primero ejecute pack() para generar un resultado.")
        self.result.plot()

    def report(self, verbose: bool = False) -> str:
        """
        Genera un reporte en formato texto con la asignación de items en cada bin y las métricas.
        :param verbose: Si es True, se incluye un reporte detallado.
        :raises ValueError: Si pack() no se ha ejecutado previamente.
        :return: Reporte en formato string.
        """
        if self.result is None:
            raise ValueError("Primero ejecute pack() para generar un resultado.")
        return self.result.report(verbose=verbose)
