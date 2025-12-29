"""Beinhaltet den Sterne-Popup."""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtSvgWidgets import QSvgWidget


class StarViewPopup(QDialog):
    """
    Ein Popup, um Infos zu einem bestimmten Stern zu zeigen.
    """

    def __init__(self, name: str, temperature: int, magnitude: int, diagram_img_path: str, raw_img_path: str):
        super().__init__()
        self.setWindowTitle(f"{name} - Infos")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        name_label = QLabel(f"Star name {name}")
        layout.addWidget(name_label)

        magnitude_label = QLabel(f"Magnitude {magnitude}")
        layout.addWidget(magnitude_label)

        temperature_label = QLabel(f"Temperature {temperature}")
        layout.addWidget(temperature_label)

        diagram_img = QSvgWidget(diagram_img_path)
        layout.addWidget(diagram_img)

        self.setLayout(layout)

def open_star_view_popup(name: str, temperature: int, magnitude: int, diagram_img_path: str, raw_img_path: str) -> None:
    """Eine Funktion um ein Sterne-Popup zu öffnen."""

    popup = StarViewPopup(name, temperature, magnitude, diagram_img_path, raw_img_path)
    popup.exec()