from typing import List, Dict, Any
from optimalbins.models.bin import Bin

class PackingResult:
    def __init__(self, bins: List[Bin], metrics: Dict[str, Any]) -> None:
        """
        :param bins: Lista de objetos Bin con los items asignados.
        :param metrics: Diccionario con métricas y estadísticas del empaquetado.
        """
        self.bins: List[Bin] = bins
        self.metrics: Dict[str, Any] = metrics

    def plot(self) -> None:
        """
        Genera una visualización del empaquetado.
        
        Para el caso 2D se utiliza matplotlib, tomando como referencia la funcionalidad de GreedyPacker y BinPacking2D.
        En el caso 3D se podría extender usando, por ejemplo, matplotlib mplot3d o plotly.
        Nota: Se asume que cada item tiene atributos de posición (x, y) asignados por el algoritmo.
        """
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        for bin in self.bins:
            fig, ax = plt.subplots()
            ax.set_title(f"Bin {bin.id}")
            # Dibujar el contorno del bin (caso 2D)
            bin_rect = Rectangle((0, 0), bin.width, bin.height, fill=None, edgecolor="black", linewidth=2)
            ax.add_patch(bin_rect)
            
            # Dibujar cada item. Se asume que cada item tiene atributos 'x' e 'y'
            for item in bin.items:
                # Si el item no tiene posición asignada, se usará (0, 0) como placeholder
                x = getattr(item, 'x', 0)
                y = getattr(item, 'y', 0)
                item_rect = Rectangle((x, y), item.width, item.height, 
                                      fill=True, edgecolor="blue", alpha=0.5)
                ax.add_patch(item_rect)
                # Mostrar el id del item en el centro del rectángulo
                ax.text(x + item.width/2, y + item.height/2, str(item.id), 
                        ha="center", va="center", fontsize=8, color="white")
            
            ax.set_xlim(0, bin.width)
            ax.set_ylim(0, bin.height)
            ax.set_xlabel("Ancho")
            ax.set_ylabel("Alto")
            plt.show()

    def report(self, verbose: bool = False) -> str:
        """
        Genera un reporte en formato texto con la asignación de items en cada bin y las métricas.
        Se inspira en los reportes de GreedyPacker y otras librerías de referencia.
        
        :param verbose: Si es True, se incluyen detalles de cada item.
        :return: Reporte en formato string.
        """
        report_lines = ["Reporte de Empaquetado:"]
        for bin in self.bins:
            report_lines.append(f"- {bin}: {len(bin.items)} items")
            if verbose:
                for item in bin.items:
                    report_lines.append(f"    * {item}")
        report_lines.append("Métricas:")
        for key, value in self.metrics.items():
            report_lines.append(f"    {key}: {value}")
        return "\n".join(report_lines)
