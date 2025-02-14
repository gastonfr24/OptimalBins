# OptimalBins 📦🔢

OptimalBins es una biblioteca de Python diseñada para abordar y resolver problemas de *bin packing*. Proporciona implementaciones de algoritmos eficientes y herramientas de visualización para optimizar la distribución de objetos en contenedores de capacidad limitada.

## Características

- **Algoritmos de Bin Packing**: Implementación de estrategias como *First-Fit Decreasing (FFD)* y *Best-Fit Decreasing (BFD)* para una asignación óptima.
- **Visualización**: Herramientas integradas para representar gráficamente los resultados de los algoritmos.
- **Modularidad**: Código organizado en módulos (`algorithms`, `common`, `demos`, `models`, `visualization`) para facilitar la extensión y el mantenimiento.

## Instalación

### Requisitos Previos

- Python 3.7 o superior.
- `matplotlib==3.10.0` para las funcionalidades de visualización.

### Instalación desde el Repositorio

1. Clona el repositorio:

   ```bash
   git clone https://github.com/gastonfr24/OptimalBins.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd OptimalBins
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso Básico

A continuación, se muestra un ejemplo de cómo utilizar el algoritmo *First-Fit Decreasing* y visualizar los resultados:

```python
from optimalbins.algorithms.first_fit_decreasing import first_fit_decreasing
from optimalbins.visualization.plot_bins import plot_bins

# Lista de pesos de los objetos
weights = [4, 8, 1, 4, 2, 1]

# Capacidad máxima de cada contenedor
bin_capacity = 10

# Ejecutar el algoritmo FFD
bins = first_fit_decreasing(weights, bin_capacity)

# Mostrar los resultados
print(f"Se requieren {len(bins)} contenedores.")
for i, bin in enumerate(bins, 1):
    print(f"Contenedor {i}: {bin}")

# Visualizar los resultados
plot_bins(bins, bin_capacity)
```

Este script organiza los objetos según el algoritmo FFD y muestra una representación gráfica de la distribución en los contenedores.

## Ejemplos Adicionales

Puedes encontrar más ejemplos prácticos en el directorio `demos` del repositorio. Estos scripts demuestran diferentes casos de uso y escenarios aplicados.

## Pruebas

El directorio `tests` contiene casos de prueba para validar la funcionalidad de los algoritmos y módulos. Para ejecutar las pruebas:

```bash
python -m unittest discover tests
```

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar o ampliar la funcionalidad de OptimalBins:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad: `git checkout -b feature/nueva-funcionalidad`.
3. Realiza tus cambios y haz commit: `git commit -m 'Añadir nueva funcionalidad'`.
4. Envía un pull request describiendo tus modificaciones.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

**Gastón Franco**  
Correo: [gastonfr24@gmail.com](mailto:gastonfr24@gmail.com)  
Repositorio: [https://github.com/gastonfr24/OptimalBins](https://github.com/gastonfr24/OptimalBins)