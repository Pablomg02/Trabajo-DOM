import numpy as np
import json

class Track:
    """
    Clase que representa un circuito compuesto por segmentos.
    Permite cargar los segmentos desde un archivo JSON.
    """
    def __init__(self, segments):
        """
        Inicializa el circuito con una lista de segmentos.
        :param segments: Lista de tuplas (longitud, radio)
        """
        self.segments = segments  # Lista de tuplas (longitud, radio)

    @classmethod
    def from_json(cls, file_path):
        """
        Crea una instancia de Track a partir de un archivo JSON.
        :param file_path: Ruta al archivo JSON
        :return: Instancia de Track
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Cada segmento es un dict con 'length' y 'radius'
        segments = []
        for seg in data['segments']:
            length = seg['length']
            radius = seg['radius']
            # tratar valores muy grandes como rectas infinitas
            if radius >= 1e12:
                radius = np.inf
            segments.append((length, radius))
        return cls(segments)

    @classmethod
    def example_track(cls):
        """
        Genera un circuito de ejemplo con rectas y curvas.
        :return: Instancia de Track
        """
        return cls([
            (300, np.inf),   # recta de 300 m
            (100, 50),       # curva de 100 m, radio 50 m
            (200, np.inf),   # recta de 200 m
            (150, 30),       # curva de 150 m, radio 30 m
        ])
