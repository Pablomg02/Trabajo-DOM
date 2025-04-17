import json

class Car:
    """
    Clase que representa un coche para la simulación de vueltas.
    Permite cargar sus parámetros desde un archivo JSON.
    """
    def __init__(self, mass, tire_grip, power, brake_force):
        """
        Inicializa el coche con los parámetros principales.
        :param mass: Masa del coche en kg
        :param tire_grip: Coeficiente de agarre de los neumáticos
        :param power: Potencia máxima (W)
        :param brake_force: Fuerza máxima de frenado (N)
        """
        self.mass = mass
        self.tire_grip = tire_grip
        self.power = power
        self.brake_force = brake_force

    @classmethod
    def from_json(cls, file_path):
        """
        Crea una instancia de Car a partir de un archivo JSON.
        :param file_path: Ruta al archivo JSON
        :return: Instancia de Car
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(
            mass=data['mass'],
            tire_grip=data['tire_grip'],
            power=data['power'],
            brake_force=data['brake_force']
        )

    def max_acceleration(self, v):
        """
        Calcula la aceleración máxima del coche (m/s^2) a una velocidad dada v (m/s).
        Considera el límite por agarre y por potencia.
        :param v: Velocidad actual (m/s)
        :return: Aceleración máxima (m/s^2)
        """
        grip_limit = self.tire_grip * 9.81 # Maxima aceleración que permiten los neumáticos

        power_limit = self.power / (self.mass * v) if v > 0 else float('inf')  # Aceleración por potencia

        return min(grip_limit, power_limit)

    def max_deceleration(self):
        """
        Calcula la desaceleración máxima del coche (m/s^2, valor negativo).
        Considera el límite por freno y por agarre.
        :return: Desaceleración máxima (m/s^2, valor negativo)
        """
        grip_limit = self.tire_grip * 9.81
        brake_limit = self.brake_force / self.mass
        return -min(grip_limit, brake_limit)
