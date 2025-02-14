# config.py

# Indica si se deben generar reportes detallados
VERBOSE: bool = True

# Algoritmo por defecto a usar (podría ser una cadena o directamente una referencia a la clase)
DEFAULT_ALGORITHM: str = "FirstFit2D"

# Dimensión por defecto para el empaquetado ("2D" o "3D")
DEFAULT_DIMENSION: str = "2D"

# Otros parámetros globales que puedan ser útiles (por ejemplo, tiempos límite, criterios de ordenación, etc.)
TIMEOUT: float = 10.0  # tiempo máximo en segundos para ejecutar un empaquetado (opcional)

# Cantidad de decimales a redondear
DEFAULT_NUMBER_OF_DECIMALS = 3