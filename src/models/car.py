import json
from .aero import Aero


class Car:
    """
    Clase que representa un coche para la simulación de vueltas.
    Permite cargar sus parámetros desde un archivo JSON.
    """
    def __init__(self, mass, tire_grip, power, brake_force, aero, brake_bias, wheelbase, h_cg):
        """
        Inicializa el coche con los parámetros principales.
        :param mass: Masa del coche en kg
        :param tire_grip: Coeficiente de agarre de los neumáticos
        :param power: Potencia máxima (W)
        :param brake_force: Fuerza máxima de frenado (N)
        :param brake_bias: Reparto de frenada (proporción al eje delantero, 0-1)
        :param wheelbase: Distancia entre ejes (m)
        :param h_cg: Altura del centro de gravedad (m)
        """
        self.mass = mass
        self.tire_grip = tire_grip
        self.power = power
        self.brake_force = brake_force
        self.aero = aero
        self.brake_bias = brake_bias  # 0.6 = 60% delante, 40% detrás
        self.wheelbase = wheelbase
        self.h_cg = h_cg

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
        Considera el límite por freno, agarre, downforce aerodinámico y reparto de frenada.
        Se asegura de que en ningún eje se supere el agarre admitido.
        :param v: Velocidad actual (m/s)
        :return: Desaceleración máxima (m/s^2, valor negativo)
        """
        g = 9.81
        downforce = self.aero.downforce(v)
        total_weight = self.mass * g + downforce

        # Límite de frenada del sistema
        a_system = self.brake_force / self.mass
        # Inicializar desaceleración con límite de sistema
        a = a_system

        # Iterar para ajustar transferencia de carga y distribución de frenada
        for _ in range(10):
            # Transferencia de peso durante la frenada
            delta_w = self.mass * a * self.h_cg / self.wheelbase
            w_front = total_weight * 0.5 + delta_w
            w_rear = total_weight * 0.5 - delta_w

            # Límite de agarre en cada eje
            grip_front = self.tire_grip * w_front
            grip_rear = self.tire_grip * w_rear

            # Evitar divisiones por cero en bias
            bias_f = self.brake_bias if self.brake_bias > 0 else 1e-3
            bias_r = (1 - self.brake_bias) if (1 - self.brake_bias) > 0 else 1e-3

            # Desaceleraciones máximas permitidas por agarre en cada eje con distribución de frenada
            a_front_limit = grip_front / (self.mass * bias_f)
            a_rear_limit = grip_rear / (self.mass * bias_r)

            # Tomar el menor entre límite del sistema y de cada eje
            a_allowed = min(a_system, a_front_limit, a_rear_limit)
            # Comprobar convergencia
            if abs(a_allowed - a) < 1e-3:
                a = a_allowed
                break
            a = a_allowed

        # Retornar desaceleración negativa
        return -a

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
            aero=aero,
            brake_bias=data.get('brake_bias', 0.6),
            wheelbase=data.get('wheelbase', 3.0),
            h_cg=data.get('h_cg', 0.3)
        )