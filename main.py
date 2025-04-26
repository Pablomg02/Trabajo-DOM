#### IMPORTAR LIBRERIAS ####
import os
from src.models.car import Car
from src.models.track import Track
from src.simulator.lap_simulator import LapSimulator
import matplotlib.pyplot as plt
import numpy as np

#### CARGAR COCHE Y CIRCUITO ####
car_path = os.path.join(os.path.dirname(__file__), "car.json")
track_path = os.path.join(os.path.dirname(__file__), "track.json")

car = Car.from_json(car_path) # Este es el coche inicial, y luego la optimización lo cambia
track = Track.from_json(track_path)

car.aero.set_aoa(-4)  # Ignorad esto de momento
 

#### EJEMPLO DE MODIFICAR UN PARÁMETRO DEL COCHE ####
car.power = 100000  # Cambiar la potencia máxima a 100 kW
car.brake_force = 5000  # Cambiar la fuerza de frenado a 5000 N

# Crear simulador de vueltas y ejecutar simulación
simulator = LapSimulator(car, track)
lap_time, v = simulator.simulate_lap()




# Mostrar el resultado por pantalla
print(f"Tiempo de vuelta: {lap_time:.2f} s")

t = np.linspace(0, lap_time, len(v), endpoint=True)

plt.plot(t, v, label="Velocidad (m/s)")
plt.show()
