
"""
POR HACER
- Hay que ver de meter las curvas de cl vs angle y cd vs angle en el json del coche"""

"""
Se asume que no hay cambios en el angulo del coche a pesar de las fuerzas, y tambien que la carga en las ruedas es igual
Aun asi, estaba bien modelar esto mejor con el modelo de bicicleta
"""

class Aero:

    def __init__(self, fw_cl, rw_cl, fw_area, rw_area, fw_cd, rw_cd):
        """
        Inicializa el modelo aerodinámico del coche.
        :param fw_cl: Coeficiente de sustentación frontal
        :param rw_cl: Coeficiente de sustentación trasera
        :param fw_area: Área frontal (m^2)
        :param rw_area: Área trasera (m^2)
        :param fw_cd: Coeficiente de arrastre frontal
        :param rw_cd: Coeficiente de arrastre trasero
        """
        self.fw_cl = fw_cl
        self.rw_cl = rw_cl
        self.fw_area = fw_area
        self.rw_area = rw_area
        self.fw_cd = fw_cd
        self.rw_cd = rw_cd
        self.rho = 1.225
        self.g = 9.81
        
    def downforce(self, v):
        """
        Calcula la fuerza de sustentación (downforce) del coche.
        :param v: Velocidad del coche (m/s)
        :return: Fuerza de sustentación (N)
        """
        return 0.5 * self.rho * v**2 * (self.fw_cl * self.fw_area + self.rw_cl * self.rw_area)
    

    def drag(self, v):
        """
        Calcula la fuerza de arrastre del coche.
        :param v: Velocidad del coche (m/s)
        :return: Fuerza de arrastre (N)
        """
        return 0.5 * self.rho * v**2 * (self.fw_cd * self.fw_area + self.rw_cd * self.rw_area)