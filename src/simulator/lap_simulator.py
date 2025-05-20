import numpy as np
import matplotlib.pyplot as plt

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
        self.v_max = self._v_max()
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
    

    def plot_lap(self, label : str | None = None):
        """
        Plots the speed profile of the lap.
        """
        _, v = self.simulate_lap()

        if label is None:
            plt.plot(v)
        else:
            plt.plot(v, label=label)
        
        plt.xlabel("Track Position (m)")
        plt.ylabel("Speed (m/s)")
        plt.grid()
        plt.legend()

    

    def _v_max(self):
        # Compute max speed at each point considering downforce (aero)
        v_max = np.zeros(len(self.radii))
        v_guess = 0.0  # Initial guess for the first point
        VEL_MAX_LIMIT = 200.0  # Límite superior  para velocidad máxima (evitar NaN o inf)
        for i, radius in enumerate(self.radii):
            # Use previous step's v_max as initial guess for smoother convergence
            if i > 0:
                v_guess = v_max[i-1]
            for _ in range(10):
                v_new = self.car.max_velocity(radius, v_guess)
                if not np.isfinite(v_new):
                    v_new = VEL_MAX_LIMIT
                if abs(v_new - v_guess) < 1e-3:
                    break
                v_guess = v_new
            # Si la velocidad sigue siendo infinita o NaN, la limitamos
            if not np.isfinite(v_guess):
                v_guess = VEL_MAX_LIMIT
            v_max[i] = v_guess
        return v_max

    def _forward(self):
        # Ensure acceleration does not exceed engine and grip limits
        for i in range(1, len(self.v)):
            a_max = self.car.max_acceleration(self.v[i-1])
            v_allowed = np.sqrt(self.v[i-1]**2 + 2 * a_max * self.delta_s)
            if v_allowed < self.v[i]:
                self.v[i] = v_allowed

    def _backward(self):
        # Ensure deceleration does not exceed braking and grip limits
        for i in range(len(self.v) - 2, -1, -1):
            decel = abs(self.car.max_deceleration(self.v[i+1]))
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

