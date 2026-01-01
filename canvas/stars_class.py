"""Nützliche dataclasses, um mit Daten zu interagieren."""

from dataclasses import dataclass

@dataclass
class Star:
    """Daten eines Sternes."""

    name: str
    temperature: float
    magnitude: float
    spec_raw: str
    spec_diagram: str