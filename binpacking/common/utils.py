from decimal import Decimal
from typing import Any

def get_limit_number_of_decimals(number_of_decimals: int) -> Decimal:
    """
    Devuelve un Decimal que sirve como límite para el número de decimales.
    Por ejemplo, si number_of_decimals es 3, retorna Decimal('1.000').
    """
    return Decimal("1." + "0" * number_of_decimals)

def set_to_decimal(value: float, number_of_decimals: int) -> Decimal:
    """
    Convierte un número a Decimal con el número de decimales especificado.
    """
    quant = get_limit_number_of_decimals(number_of_decimals)
    return Decimal(value).quantize(quant)

def rect_intersect(item1: Any, item2: Any, axis1: int, axis2: int) -> bool:
    """
    Determina si dos proyecciones rectangulares de los items se intersectan
    en los ejes dados (por ejemplo, ancho-alto, alto-profundidad, etc.).
    
    Se utilizan las dimensiones actuales de los items (obtenidas mediante get_dimension())
    y sus posiciones.
    
    :param item1: Primer item (debe tener get_dimension() y position como tupla).
    :param item2: Segundo item.
    :param axis1: Índice del primer eje (por ejemplo, 0 para ancho).
    :param axis2: Índice del segundo eje (por ejemplo, 1 para alto).
    :return: True si se intersectan en la proyección definida por los dos ejes.
    """
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()
    
    # Calcular el centro en el eje axis1 y axis2 para cada item.
    c1_axis1 = item1.position[axis1] + d1[axis1] / 2
    c1_axis2 = item1.position[axis2] + d1[axis2] / 2
    c2_axis1 = item2.position[axis1] + d2[axis1] / 2
    c2_axis2 = item2.position[axis2] + d2[axis2] / 2
    
    # Distancia entre centros en cada eje.
    dist_axis1 = abs(c1_axis1 - c2_axis1)
    dist_axis2 = abs(c1_axis2 - c2_axis2)
    
    # Dos rectángulos se intersectan si la distancia entre centros es menor que
    # la suma de la mitad de sus dimensiones en cada eje.
    return (dist_axis1 < (d1[axis1] + d2[axis1]) / 2) and (dist_axis2 < (d1[axis2] + d2[axis2]) / 2)

def intersect(item1: Any, item2: Any) -> bool:
    """
    Determina si dos items se intersectan en 3D.
    Se evalúan las intersecciones en las proyecciones:
      - Ancho vs. Alto,
      - Alto vs. Profundidad,
      - Ancho vs. Profundidad.
    
    Se asume que existen constantes definidas en 'constants' para los índices:
      Axis.WIDTH, Axis.HEIGHT y Axis.DEPTH.
    
    :param item1: Primer item.
    :param item2: Segundo item.
    :return: True si los items se intersectan en las tres proyecciones; False en caso contrario.
    """
    from .constants import Axis
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )