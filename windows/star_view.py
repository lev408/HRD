"""Beinhaltet den Sterne-Popup."""
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QResizeEvent, QPainter
from PySide6.QtSvgWidgets import QSvgWidget
import numpy as np
from astropy.io import fits
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer

class AspectRatioLabel(QLabel):
    """
    Ein angepasstes Label, das das Bild beim Skalieren des Fensters
    automatisch anpasst, dabei aber das Seitenverhältnis beibehält.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_pixmap = None
        # Wichtig: Erlaubt dem Label, kleiner zu werden als das Bild
        self.setMinimumSize(1, 1)
        # Wir kümmern uns selbst um das Skalieren, daher False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)

    def setPixmap(self, pixmap: QPixmap):
        # Wir speichern das Original, um Qualitätsverlust beim Skalieren zu vermeiden
        self._original_pixmap = pixmap
        self._update_pixmap()

    def resizeEvent(self, event: QResizeEvent):
        # Wird aufgerufen, wenn sich die Größe des Widgets ändert
        self._update_pixmap()
        super().resizeEvent(event)

    def _update_pixmap(self):
        if self._original_pixmap and not self._original_pixmap.isNull():
            # Skaliere das Bild auf die aktuelle Größe des Labels
            # Qt.KeepAspectRatio sorgt dafür, dass es nicht verzerrt wird
            # Qt.SmoothTransformation sorgt für bessere Qualität (Anti-Aliasing)
            scaled_pixmap = self._original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            super().setPixmap(scaled_pixmap)

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

        def svg_to_pixmap(svg_path: str, width=1000) -> QPixmap:
            """
            Lädt ein SVG und rendert es in eine hochauflösende QPixmap.
            Dadurch können wir es im AspectRatioLabel wie ein normales Bild behandeln.
            """
            renderer = QSvgRenderer(svg_path)
            if not renderer.isValid():
                return QPixmap()

            # Berechne Höhe basierend auf Seitenverhältnis des SVGs
            default_size = renderer.defaultSize()
            height = int(width * (default_size.height() / default_size.width()))

            # Erstelle leere Pixmap mit transparentem Hintergrund
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)

            # Male das SVG auf die Pixmap
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()

            return pixmap

        #diagram_img = QSvgWidget(diagram_img_path)
        #diagram_img = QSvgWidget(f"images/{name}.svg")
        #diagram_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #layout.addWidget(diagram_img)

        svg_pixmap = svg_to_pixmap(f"images/{name}.svg")

        if not svg_pixmap.isNull():
            diagram_label = AspectRatioLabel()
            diagram_label.setPixmap(svg_pixmap)
            layout.addWidget(diagram_label)
        else:
            layout.addWidget(QLabel("Diagramm konnte nicht geladen werden"))

        try:
            #hdu_list = fits.open(raw_img_path)
            hdu_list = fits.open(f"images/{name}.fit")
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
                width,
                height,
                width,
                QImage.Format_Grayscale8
            )
            pixmap = QPixmap.fromImage(qimage)
            raw_label = AspectRatioLabel() #QLabel("Spectrum raw")
            raw_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            raw_label.setPixmap(pixmap)
            layout.addWidget(raw_label)

        except Exception as e:
            print(f"Fehler: {e}")


        self.setLayout(layout)


def open_star_view_popup(name: str, temperature: int, magnitude: int, diagram_img_path: str, raw_img_path: str) -> None:
    """Eine Funktion um ein Sterne-Popup zu öffnen."""

    popup = StarViewPopup(name, temperature, magnitude, diagram_img_path, raw_img_path)
    popup.exec()