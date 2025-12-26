from dataclasses import dataclass
'''
class Star:
    def __init__(self, name, temperature, magnitude, spec_raw, spec_diagram):
        self.name = name
        self.temperature = temperature
        self.magnitude = magnitude
        self.spec_raw = spec_raw
        self.spec_diagram = spec_diagram
'''

@dataclass
class Star:
    name: str
    temperature: float
    magnitude: float
    spec_raw: str
    spec_diagram: str