import os
from src.models.car import Car
from src.models.track import Track
from src.simulator.lap_simulator import LapSimulator
import matplotlib.pyplot as plt
import numpy as np


car_path = os.path.join(os.path.dirname(__file__), "car.json")
track_path = os.path.join(os.path.dirname(__file__), "track.json")

# Cargar coche y circuito desde archivos JSON
car = Car.from_json(car_path)
track = Track.from_json(track_path)
 
# Crear simulador de vueltas y ejecutar simulación
simulator = LapSimulator(car, track)
lap_time, v = simulator.simulate_lap()

# Mostrar el resultado por pantalla
print(f"Tiempo de vuelta: {lap_time:.2f} s")

t = np.linspace(0, lap_time, len(v), endpoint=True)

plt.plot(t, v, label="Velocidad (m/s)")
plt.show()
