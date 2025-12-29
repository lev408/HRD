"""Beinhaltet den Graph-Zeiger."""

from PySide6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT


class GraphViewWindow(QWidget):
    """
    Zeigt den mitgegebenen Graphen, beinhaltet auch eine Toolbar um mit ihm zu interagieren.

    :param canvas: Der Graph, der vom Anzeiger angezeigt wird.
    """

    def __init__(self, canvas: FigureCanvasQTAgg):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar2QT(canvas, self))
        layout.addWidget(canvas)
        self.setLayout(layout)
