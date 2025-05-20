import json
import numpy as np
import matplotlib.pyplot as plt

def plot_track(track_file):
    with open(track_file, 'r') as f:
        data = json.load(f)

    segments = data['segments']
    x, y = 0.0, 0.0
    heading = 0.0  # Ángulo en radianes
    xs, ys = [x], [y]

    for segment in segments:
        length = segment['length']
        radius = segment['radius']

        if np.isinf(radius):  # recta
            dx = length * np.cos(heading)
            dy = length * np.sin(heading)
            x += dx
            y += dy
            xs.append(x)
            ys.append(y)

        else:  # curva circular
            angle = length / radius  # ángulo barrido
            # centro de la circunferencia
            cx = x - radius * np.sin(heading)
            cy = y + radius * np.cos(heading)

            # puntos a lo largo del arco
            arc = np.linspace(0, angle, num=50)
            for a in arc[1:]:
                new_heading = heading + a
                new_x = cx + radius * np.sin(new_heading)
                new_y = cy - radius * np.cos(new_heading)
                xs.append(new_x)
                ys.append(new_y)
            # actualizar posición y orientación final
            heading += angle
            x = xs[-1]
            y = ys[-1]

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(xs, ys, linewidth=1)
    plt.title("Representación del Circuito")
    plt.axis('equal')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid(True)
    plt.show()

# Usar con el archivo dado
plot_track('track.json')
