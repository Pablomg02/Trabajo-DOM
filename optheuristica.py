#### IMPORTAR LIBRERIAS ####
import os
import numpy as np
import matplotlib.pyplot as plt
from geneticalgorithm import geneticalgorithm as ga

from src.models.car import Car
from src.models.track import Track
from src.simulator.lap_simulator import LapSimulator

#### CARGAR COCHE Y CIRCUITO ####
car_path = os.path.join(os.path.dirname(__file__), "car.json")
track_path = os.path.join(os.path.dirname(__file__), "track.json")

track = Track.from_json(track_path)

#### DEFINIR FUNCIÓN DE FITNESS MULTIVARIABLE ####
def fitness_function(X):
    power = X[0]
    brake_force = X[1]
    
    
    car = Car.from_json(car_path)
    car.power = power
    car.brake_force = brake_force


    try:
        simulator = LapSimulator(car, track)
        lap_time, v = simulator.simulate_lap()
        if lap_time is None or np.isnan(lap_time) or lap_time > 1e4:
            return 1e6
        return lap_time
    except:
        return 1e6

#### PARÁMETROS DEL ALGORITMO GENÉTICO ####
varbound = np.array([
    [8000, 15000],     # power (W)
    [3000, 10000],     # brake_force (N)

])

algorithm_param = {
    'max_num_iteration': 60,
    'population_size': 30,
    'mutation_probability': 0.1,
    'elit_ratio': 0.02,
    'crossover_probability': 0.5,
    'parents_portion': 0.3,
    'crossover_type': 'uniform',
    'max_iteration_without_improv': 15
}

model = ga(
    function=fitness_function,
    dimension=2,  # Ahora optimizamos 3 variables
    variable_type='real',
    variable_boundaries=varbound,
    algorithm_parameters=algorithm_param
)

#### EJECUTAR OPTIMIZACIÓN ####
model.run()

#### SACAR EL MEJOR SETUP ####
best_setup = model.output_dict['variable']
best_time = model.output_dict['function']

print("\nMejor configuración encontrada:")
print(f"Power óptimo: {best_setup[0]:.2f} W")
print(f"Brake force óptimo: {best_setup[1]:.2f} N")

print(f"Tiempo de vuelta correspondiente: {best_time:.2f} segundos")

#### VISUALIZAR EVOLUCIÓN ####
convergence = model.report

plt.plot(convergence)
plt.xlabel("Iteraciones")
plt.ylabel("Tiempo de vuelta (s)")
plt.title("Optimización multivariable")
plt.grid()
plt.show()
