"""Beinhaltet den Sterne-Popup."""
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
import numpy as np
from astropy.io import fits
from PySide6.QtCore import Qt

class StarViewPopup(QDialog):
    """
    Ein Popup, um Infos zu einem bestimmten Stern zu zeigen.
    """

    def __init__(self, name: str, temperature: int, magnitude: int, diagram_img_path: str, raw_img_path: str):
        super().__init__()
        self.setWindowTitle(f"{name} - Infos")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        name_label = QLabel(f"Name des Sterns: {name}")
        layout.addWidget(name_label)

        magnitude_label = QLabel(f"Absolute Helligkeit: {magnitude}mag")
        layout.addWidget(magnitude_label)

        temperature_label = QLabel(f"Temperatur: {temperature}K")
        layout.addWidget(temperature_label)

        diagram_img = QSvgWidget(diagram_img_path)
        layout.addWidget(diagram_img)

        try:
            hdu_list = fits.open(raw_img_path)
            hdu_list.info()
            image_data = hdu_list[0].data
            print(image_data)
            print(image_data.ndim)
            hdu_list.close()

            image_data = np.nan_to_num(image_data)
            image_data = image_data - image_data.min()
            image_data = image_data / image_data.max()
            image_data = (image_data * 255).astype(np.uint8)

            height, width = image_data.shape
            qimage = QImage(
                image_data.data,
                width//3,
                height//3,
                width,
                QImage.Format_Grayscale8
            )
            pixmap = QPixmap.fromImage(qimage)
            raw_label = QLabel("Spectrum raw")
            raw_label.setPixmap(pixmap)
            raw_label.setScaledContents(True)
            layout.addWidget(raw_label)

        except Exception as e:
            print(f"Fehler: {e}")

        self.setLayout(layout)


def open_star_view_popup(name: str, temperature: int, magnitude: int, diagram_img_path: str, raw_img_path: str) -> None:
    """Eine Funktion um ein Sterne-Popup zu öffnen."""

    popup = StarViewPopup(name, temperature, magnitude, diagram_img_path, raw_img_path)
    popup.exec()