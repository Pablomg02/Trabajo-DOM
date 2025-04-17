import numpy as np

class LapSimulator:
    """
    Clase principal para simular una vuelta en un circuito dado un coche y un circuito.
    """
    def __init__(self, car, track, delta_s=1.0):
        """
        Inicializa el simulador de vueltas.
        :param car: Instancia de Car
        :param track: Instancia de Track
        :param delta_s: Resolución espacial (m)
        """
        self.car = car
        self.track = track
        self.delta_s = delta_s  # Resolución espacial (m)


    def simulate_lap(self):
        # Discretize track into curvature radii per step
        self.radii = self._discretize()
        # Compute max speed due to lateral grip at each point
        radii_arr = np.array(self.radii, dtype=float)
        self.v_max = np.sqrt(self.car.tire_grip * 9.81 * radii_arr)
        # Initialize speed profile with curvature limits
        self.v = self.v_max.copy()
        # Start from standstill
        self.v[0] = 0.0
        # Forward pass: acceleration limits
        self._forward()
        # Backward pass: braking limits
        self._backward()
        # Calculate lap time using trapezoidal integration
        return self._calculate_lap_time(), self.v

    def _forward(self):
        # Ensure acceleration does not exceed engine and grip limits
        for i in range(1, len(self.v)):
            a_max = self.car.max_acceleration(self.v[i-1])
            v_allowed = np.sqrt(self.v[i-1]**2 + 2 * a_max * self.delta_s)
            if v_allowed < self.v[i]:
                self.v[i] = v_allowed

    def _backward(self):
        # Ensure deceleration does not exceed braking and grip limits
        decel = abs(self.car.max_deceleration())
        for i in range(len(self.v) - 2, -1, -1):
            v_allowed = np.sqrt(self.v[i+1]**2 + 2 * decel * self.delta_s)
            if v_allowed < self.v[i]:
                self.v[i] = v_allowed

    def _calculate_lap_time(self):
        # Compute total lap time via trapezoidal rule
        time = 0.0
        for i in range(len(self.v) - 1):
            v1, v2 = self.v[i], self.v[i+1]
            if v1 + v2 > 0:
                time += 2 * self.delta_s / (v1 + v2)
        return time

    def _discretize(self):
        # Create list of curvature radii for each spatial step
        radii = []
        for length, radius in self.track.segments:
            # Number of steps in this segment
            steps = int(np.ceil(length / self.delta_s))
            radii.extend([radius] * steps)
        return radii

