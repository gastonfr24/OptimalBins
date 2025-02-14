from typing import Optional, Tuple, Union, List
from itertools import permutations
from common.constants import RotationType
from config import DEFAULT_NUMBER_OF_DECIMALS

START_POSITION = [0, 0, 0]

class Item:
    def __init__(
        self,
        id: str,
        width: float,
        height: float,
        depth: Optional[float] = None,
        weight: Optional[float] = None,
        rotations_allowed: bool = True,
        name: Optional[str] = None
    ) -> None:
        """
        :param id: Identificador único del item.
        :param width: Ancho del item.
        :param height: Alto del item.
        :param depth: Profundidad del item (opcional; si es None, se asume 2D).
        :param weight: Peso del item (opcional).
        :param rotations_allowed: Indica si se permiten rotaciones para optimizar el empaquetado.
        :param name: Nombre del item (opcional; por defecto se usa el id).
        """
        self.id: str = id
        self.width: float = width
        self.height: float = height
        self.depth: Optional[float] = depth
        self.weight: Optional[float] = weight
        self.rotations_allowed: bool = rotations_allowed
        self.name: str = name if name is not None else id

        # Posición: si depth es None se asume 2D (solo x, y); en 3D se usará (x, y, z)
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: Optional[float] = 0.0 if depth is not None else None

        # Atributo para determinar la orientación actual. Por defecto, RT_WHD (ancho, alto, profundidad)
        self.rotation_type: int = RotationType.RT_WHD

        # Número de decimales para formatear (opcional, se usa en 3dbinpacking)
        self.number_of_decimals: int = DEFAULT_NUMBER_OF_DECIMALS

    def set_position(self, x: float, y: float, z: Optional[float] = None) -> None:
        """
        Establece la posición del item dentro de un bin.

        :param x: Coordenada x.
        :param y: Coordenada y.
        :param z: Coordenada z (opcional, solo se usa si depth está definido).
        """
        self.x = x
        self.y = y
        if self.depth is not None and z is not None:
            self.z = z

    def dimensions(self) -> Union[Tuple[float, float], Tuple[float, float, float]]:
        """
        Devuelve las dimensiones del item.
        
        Retorna (width, height) en 2D o (width, height, depth) en 3D (según la orientación actual).
        """
        if self.depth is not None:
            return self.get_dimension()
        return (self.width, self.height)

    def get_dimension(self) -> Tuple[float, float, float]:
        """
        Devuelve las dimensiones del item basándose en su rotation_type.
        
        Los valores se interpretan según:
          - RT_WHD: (width, height, depth)
          - RT_HWD: (height, width, depth)
          - RT_HDW: (height, depth, width)
          - RT_DHW: (depth, height, width)
          - RT_DWH: (depth, width, height)
          - RT_WDH: (width, depth, height)
        """
        if self.rotation_type == RotationType.RT_WHD:
            return (self.width, self.height, self.depth)
        elif self.rotation_type == RotationType.RT_HWD:
            return (self.height, self.width, self.depth)
        elif self.rotation_type == RotationType.RT_HDW:
            return (self.height, self.depth, self.width)
        elif self.rotation_type == RotationType.RT_DHW:
            return (self.depth, self.height, self.width)
        elif self.rotation_type == RotationType.RT_DWH:
            return (self.depth, self.width, self.height)
        elif self.rotation_type == RotationType.RT_WDH:
            return (self.width, self.depth, self.height)
        else:
            return (self.width, self.height, self.depth)

    def get_volume(self) -> float:
        dims = self.dimensions()
        if len(dims) == 3:
            return dims[0] * dims[1] * dims[2]
        return dims[0] * dims[1]

    def get_orientations(self) -> List[Tuple[float, float, float]]:
        """
        Devuelve una lista de orientaciones posibles para el item.
        
        - Si el item es 2D o no se permiten rotaciones, retorna solo la orientación original,
          usando (width, height, 0) para mantener el formato 3-tuple.
        - Si se permiten rotaciones y el item es 3D, retorna todas las permutaciones únicas de (width, height, depth).
        """
        if self.depth is None or not self.rotations_allowed:
            return [(self.width, self.height, 0)]
        else:
            return list(set(permutations((self.width, self.height, self.depth), 3)))

    def __repr__(self) -> str:
        if self.depth is not None:
            return (f"Item({self.id}, {self.width}x{self.height}x{self.depth}, pos=({self.x}, "
                    f"{self.y}, {self.z}), rt={self.rotation_type})")
        return f"Item({self.id}, {self.width}x{self.height}, pos=({self.x}, {self.y}))"
