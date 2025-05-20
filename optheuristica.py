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



#### DEFINIR FUNCIÓN DE FITNESS MULTIVARIABLE ####
def fitness_function(X):
    car = Car.from_json(car_path) # Este es el coche inicial, y luego la optimización lo cambia
    track = Track.from_json(track_path)

    track = Track.from_json(track_path)

    power = X[0]
    brake_force = X[1]
    mass=X[2]
    tire_grip = X[3]
    cl_alpha_front = X[4]
    cl_alpha_rear = X[5]
    cd_alpha_front = X[6]
    cd_alpha_rear = X[7]
    fw_area = X[8]
    rw_area = X[9]


    car = Car.from_json(car_path)
    car.power = power
    car.brake_force = brake_force
    car.mass = mass
    car.tire_grip = tire_grip
    car.aero.cl_alpha_front = cl_alpha_front   
    car.aero.cl_alpha_rear = cl_alpha_rear
    car.aero.cd_alpha_front = cd_alpha_front
    car.aero.cd_alpha_rear = cd_alpha_rear
    car.aero.fw_area = fw_area
    car.aero.rw_area = rw_area


    # car.aero.set_aoa(-4)  # Ignorad esto de momento
    
    simulator = LapSimulator(car, track) 
    lap_time, v = simulator.simulate_lap()

    # print(f"[EVAL] power={power:.0f}, brake_force={brake_force:.0f}, mass={mass:.0f} --> lap_time={lap_time:.3f}")

    return lap_time

    
    # try:
    #     simulator = LapSimulator(car, track)
    #     lap_time, v = simulator.simulate_lap()
    #     # if lap_time is None or np.isnan(lap_time) or lap_time > 1e4:
    #     #     return 1e6
    #     #  # Mostrar tiempo de vuelta de cada individuo
    #     # print(f"[EVAL] power={power:.0f}, brake_force={brake_force:.0f}, mass={mass:.0f} --> lap_time={lap_time:.3f}")

    #     return lap_time
    # except Exception as e:
    #     print(f"Error during simulation: {e}")
    #     return 1e2   

#### PARÁMETROS DEL ALGORITMO GENÉTICO ####
varbound = np.array([
    [300000, 650000],     # power (W)
    [3000, 10000],     # brake_force (N)
    [600,900],     # mass (kg)
    [0.1, 2],     # tire_grip (N)
    [0.1, 1],     # cl_alpha_front (m^2/rad)
    [0.1, 1],     # cl_alpha_rear (m^2/rad)
    [0.1, 1],     # cd_alpha_front (m^2/rad)
    [0.1, 1],     # cd_alpha_rear (m^2/rad)
    [0.1, 2],     # fw_area (m^2)
    [0.1, 2]      # rw_area (m^2)
])

algorithm_param = {
    'max_num_iteration': 100,
    'population_size': 100,
    'mutation_probability': 0.1,
    'elit_ratio': 0.05,
    'crossover_probability': 0.5,
    'parents_portion': 0.3,
    'crossover_type': 'uniform',
    'max_iteration_without_improv': 10
}

model = ga(
    function=fitness_function,
    dimension=10,  # Ahora optimizamos 3 variables
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
print(f"Mass óptimo: {best_setup[2]:.2f} N")
print(f"Tire grip óptimo: {best_setup[3]:.2f} N")
print(f"Cl_alpha_front óptimo: {best_setup[4]:.2f} m^2/rad")
print(f"Cl_alpha_rear óptimo: {best_setup[5]:.2f} m^2/rad")
print(f"Cd_alpha_front óptimo: {best_setup[6]:.2f} m^2/rad")
print(f"Cd_alpha_rear óptimo: {best_setup[7]:.2f} m^2/rad")
print(f"Fw_area óptimo: {best_setup[8]:.2f} m^2")
print(f"Rw_area óptimo: {best_setup[9]:.2f} m^2")

print(f"Tiempo de vuelta correspondiente: {best_time:.2f} segundos")

#### VISUALIZAR EVOLUCIÓN ####
convergence = model.report

plt.plot(convergence)
plt.xlabel("Iteraciones")
plt.ylabel("Tiempo de vuelta (s)")
plt.title("Optimización multivariable")
plt.grid()
# plt.ylim(31,34)  # Limita el eje y de 99 a 101
plt.show()

print(f"Iteraciones realizadas: {len(model.report)}")
print(f"Iteraciones máximas: {algorithm_param['max_num_iteration']}")
print(f"Iteraciones sin mejora permitidas: {algorithm_param['max_iteration_without_improv']}")