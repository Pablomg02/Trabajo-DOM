
"""
POR HACER
- Hay que ver de meter las curvas de cl vs angle y cd vs angle en el json del coche"""

"""
Se asume que no hay cambios en el angulo del coche a pesar de las fuerzas, y tambien que la carga en las ruedas es igual
Aun asi, estaba bien modelar esto mejor con el modelo de bicicleta
"""

class Aero:

    def __init__(self, cl_alpha_front, cl_alpha_rear, cd_alpha_front, cd_alpha_rear, fw_area, rw_area):
        """
        Inicializa el modelo aerodinámico del coche.
        :param cl_alpha_front: Coeficiente de sustentación frontal (m^2/rad)
        :param cl_alpha_rear: Coeficiente de sustentación trasera (m^2/rad)
        :param cd_alpha_front: Coeficiente de arrastre frontal (m^2/rad)
        :param cd_alpha_rear: Coeficiente de arrastre trasera (m^2/rad)
        :param fw_area: Área frontal del coche (m^2)
        :param rw_area: Área trasera del coche (m^2)
        """
        self.cl_alpha_front = cl_alpha_front
        self.cl_alpha_rear = cl_alpha_rear
        self.cd_alpha_front = cd_alpha_front
        self.cd_alpha_rear = cd_alpha_rear
        self.fw_area = fw_area
        self.rw_area = rw_area

        self._aoa_front = None
        self._aoa_rear = None

        self.cl_front = None
        self.cl_rear = None
        self.cd_front = None
        self.cd_rear = None

        self.rho = 1.225  # Densidad del aire (kg/m^3) a nivel del mar y 15°C


    @property
    def aoa_front(self):
        """
        Devuelve el ángulo de ataque del coche.
        :return: Ángulo de ataque (rad)
        """
        return self._aoa_front
    
    @aoa_front.setter
    def aoa_front(self, aoa):
        """
        Establece el ángulo de ataque del coche.
        :param aoa: Ángulo de ataque (rad)
        """
        self._aoa_front = aoa

        if aoa > 15:
            self.cl_front = self.cl_alpha_front * (15 - 0.3 * (aoa - 15)) # Entrada en perdida
        else:
            self.cl_front = self.cl_alpha_front * aoa
        self.cd_front = self.cd_alpha_front * aoa + (self.cd_alpha_front*0.3) * aoa**2

    @property
    def aoa_rear(self):
        """
        Devuelve el ángulo de ataque del coche.
        :return: Ángulo de ataque (rad)
        """
        return self._aoa_rear
    
    @aoa_rear.setter
    def aoa_rear(self, aoa):
        """
        Establece el ángulo de ataque del coche.
        :param aoa: Ángulo de ataque (rad)
        """
        self._aoa_rear = aoa

        if aoa > 15:
            self.cl_rear = self.cl_alpha_rear * (15 - 0.3 * (aoa - 15)) # Entrada en perdida
        else:
            self.cl_rear = self.cl_alpha_rear * aoa
        self.cd_rear = self.cd_alpha_rear * aoa + (self.cd_alpha_rear*0.3) * aoa**2

        
    def downforce(self, v):
        """
        Calcula la fuerza de sustentación (downforce) del coche.
        :param v: Velocidad del coche (m/s)
        :return: Fuerza de sustentación (N)
        """
        return 0.5 * self.rho * v**2 * (self.cl_front * self.fw_area + self.cl_rear * self.rw_area)
    

    def drag(self, v):
        """
        Calcula la fuerza de arrastre del coche.
        :param v: Velocidad del coche (m/s)
        :return: Fuerza de arrastre (N)
        """
        return 0.5 * self.rho * v**2 * (self.cd_front * self.fw_area + self.cd_rear * self.rw_area)