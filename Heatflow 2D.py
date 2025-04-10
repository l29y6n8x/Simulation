import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import copy
from perlin_noise import PerlinNoise

first = True

# Globale Variablen
temperature, fig, axs, xCord, yCord, old_temp, dt, t = [], None, None, 0, 0, [], 0, 0
temperature_data = []
time_data = []
running = True
data_lock = threading.Lock()  # Schutz für gemeinsame Daten
a = 80.2  # Wärmeleitfähigkeit (wird in setup gesetzt)


def setup(size, time_interval, heat_conductivity):
    global temperature, fig, axs, xCord, yCord, dt, a
    dt = time_interval
    a = heat_conductivity
    noise = PerlinNoise(octaves=2)
    xCord, yCord = size, int(size / 5)

    # Erzeugung der Starttemperatur mit Perlin Noise
    temperature = [[10 * noise([i / xCord, j / yCord]) for j in range(xCord)] for i in range(yCord)]
    fig, axs = plt.subplots(2, 1, figsize=(10, 4))
    fig.tight_layout()

    # Erste Zeichnung (ohne plt.pause, da im Hauptthread gemacht wird)
    draw()


def get_next_values(x, y, maxX, maxY):
    add = 0
    asd = 0
    if y == 0:
        up = None
    else:
        up = temperature[y - 1][x]
        add = add + up
        asd += 1

    if y == maxY:
        down = None
    else:
        down = temperature[y + 1][x]
        add = add + down
        asd += 1

    if x == 0:
        left = None
    else:
        left = temperature[y][x - 1]
        add = add + left
        asd += 1

    if x == maxX:
        right = None
    else:
        right = temperature[y][x + 1]
        add = add + right
        asd += 1

    diff = add / asd - old_temp[y][x]
    return diff


def get_temp_diff(x, y, diff):
    temperature[y][x] = old_temp[y][x] + a * diff * dt


def get_avrg_temp():
    return sum(sum(row) for row in temperature) / (yCord * xCord)


def simulation_update():
    global old_temp, t, running
    while running:
        start_time = time.time()
        with data_lock:
            # Erstelle eine tiefe Kopie der Temperaturmatrix
            old_temp = copy.deepcopy(temperature)
            for i in range(yCord):
                for j in range(xCord):
                    diff = get_next_values(j, i, xCord - 1, yCord - 1)
                    get_temp_diff(j, i, diff)
            t += dt
            time_data.append(t)
            temperature_data.append(get_avrg_temp())
        # Zeitmessung und Schlafen, um Echtzeitsimulation zu erreichen
        elapsed_time = time.time() - start_time
        sleep_time = max(0, dt - elapsed_time)
        time.sleep(sleep_time)


def draw():
    global first
    # Diese Funktion wird ausschließlich im Hauptthread aufgerufen!
    with data_lock:
        axs[0].cla()
        psm = axs[0].pcolormesh(temperature, cmap='inferno', rasterized=True, vmin=-4, vmax=4)
        axs[0].set_title('Temperaturverteilung')

        if first:
            cbar = fig.colorbar(psm, ax=axs[0])
            cbar.set_label('Temperatur (K)')
            first = False

        axs[1].cla()
        axs[1].plot(time_data, temperature_data, color='red')
        axs[1].set_title('Durchschnittstemperatur über Zeit')
    fig.canvas.draw_idle()  # Aktualisiere den Canvas


# Setup der Simulation
setup(200, 0.01, 40.2)

# Starte den Simulations-Thread
sim_thread = threading.Thread(target=simulation_update)
sim_thread.start()

# GUI-Schleife im Hauptthread: Hier werden die Zeichnungen aktualisiert
try:
    while running:
        draw()
        plt.pause(0.01)  # Erlaubt dem GUI-Event-Loop, Ereignisse zu verarbeiten
except KeyboardInterrupt:
    running = False
    sim_thread.join()