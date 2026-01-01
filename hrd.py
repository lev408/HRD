"""Startet eine QT-Applikation, um den HRD Graph zu zeigen."""

import sys

from PySide6.QtWidgets import QApplication
from windows.graph_view import GraphViewWindow

from canvas.graph_canvas import GraphCanvas

if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    # Zeige das Graph Fenster
    app = GraphViewWindow(GraphCanvas())
    app.show()
    app.activateWindow()
    app.raise_()

    qapp.exec()