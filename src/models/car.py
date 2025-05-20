import json
from .aero import Aero


class Car:
    """
    Clase que representa un coche para la simulación de vueltas.
    Permite cargar sus parámetros desde un archivo JSON.
    """
    def __init__(self, mass, tire_grip, power, brake_force, aero):
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


        self.aero = aero
        

    def max_acceleration(self, v):
        """
        Calcula la aceleración máxima del coche (m/s^2) a una velocidad dada v (m/s).
        Considera el límite por agarre y por potencia.
        :param v: Velocidad actual (m/s)
        :return: Aceleración máxima (m/s^2)
        """
        # Compute forces in Newtons
        drag_force = self.aero.drag(v)
        grip_force = self.tire_grip * self.mass * 9.81  # Max traction force (N)
        # Power limit force: F = P / v, infinite at v=0 to allow initial acceleration
        power_force = self.power / v if v > 0 else float('inf')  # (N)
        # Available force limited by grip and power
        F_available = min(grip_force, power_force)
        # Net force after overcoming drag
        net_force = F_available - drag_force
        # Acceleration = net force / mass
        acc = net_force / self.mass
        # Do not allow negative acceleration
        return max(acc, 0.0)

    def max_deceleration(self, v):
        """
        Calcula la desaceleración máxima del coche (m/s^2, valor negativo).
        Considera el límite por freno, agarre y downforce aerodinámico.
        :param v: Velocidad actual (m/s)
        :return: Desaceleración máxima (m/s^2, valor negativo)
        """
        downforce = self.aero.downforce(v)
        grip_limit = self.tire_grip * (self.mass * 9.81 + downforce) / self.mass
        brake_limit = self.brake_force / self.mass

        return -min(grip_limit, brake_limit)
    

    def max_velocity(self, radius, v):
        """
        Calcula la velocidad máxima (m/s) en una curva de radio dado y velocidad actual (para downforce).
        :param radius: Radio de la curva (m)
        :param v: Velocidad actual (m/s) para calcular downforce
        :return: Velocidad máxima (m/s)
        """
        # Downforce depende de la velocidad actual
        downforce = self.aero.downforce(v)
        # Fuerza de agarre total (incluye downforce)
        grip_force = self.tire_grip * (self.mass * 9.81 + downforce)
        # v^2 = F * r / m
        vmax = (grip_force * radius / self.mass) ** 0.5
        return vmax





    @classmethod
    def from_json(cls, file_path):
        """
        Crea una instancia de Car a partir de un archivo JSON.
        :param file_path: Ruta al archivo JSON
        :return: Instancia de Car
        """
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Instanciar objeto Aero con parámetros del JSON
        aero = Aero(
            cl_alpha_front=data['cl_alpha_front'],
            cl_alpha_rear=data['cl_alpha_rear'],
            cd_alpha_front=data['cd_alpha_front'],
            cd_alpha_rear=data['cd_alpha_rear'],
            fw_area=data['fw_area'],
            rw_area=data['rw_area']
        )
        return cls(
            mass=data['mass'],
            tire_grip=data['tire_grip'],
            power=data['power'],
            brake_force=data['brake_force'],
            aero=aero
        )