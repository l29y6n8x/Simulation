import random
import keyboard
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
from time import sleep

t = 0
temperatur_data = []
time_data = []


def temps(res):
    last = 20
    randoms = []
    for i in range(res):
        # Erzeugt eine periodische Temperaturverteilung
        rand = 20 * np.cos((np.pi * 2 * 1 / r) * i)
        randoms.append(rand)
        last = rand
    return randoms


def getBig(lst):
    big = 0
    for i in range(len(lst)):
        if lst[i] > lst[big]:
            big = i
    return lst[big]


def getSmall(lst):
    small = 0
    for i in range(len(lst)):
        if lst[i] < lst[small]:
            small = i
    return lst[small]


def setup(colormap, resulution, Temperaturleitfaehigkeit, Zeitintervall):
    global axs, temp_array, temperatur, norm, x, color, r, a, dt, fig, smallest, largest
    color = colormap
    r = resulution
    a = Temperaturleitfaehigkeit
    dt = Zeitintervall

    randoms = temps(r)
    temperatur = np.array(randoms)
    print("Anzahl Temperaturwerte:", len(temperatur))
    # temp_array wird hier nicht mehr zwingend benötigt,
    # da wir direkt mit "temperatur" arbeiten.
    temp_array = [temperatur]
    x = np.linspace(0, 10, r)

    # Normalisiere die Temperaturwerte für den Scatterplot
    norm = mcolors.Normalize(vmin=temperatur.min(), vmax=temperatur.max())
    largest = getBig(temperatur)
    smallest = getSmall(temperatur)


def update():
    global temperatur, norm, t
    temp = temperatur.copy()

    # Berechne den neuen Zustand des Stabes – nur innere Punkte, um Indexprobleme zu vermeiden.
    for i in range(1, r - 1):
        temperatur[i] += a * dt * ((temp[i - 1] + temp[i + 1]) / 2 - temp[i])

    # Randbedingungen korrigieren
    temperatur[0] = temp[0] + a * dt * (temp[1] - temp[0])
    temperatur[-1] = temp[-1] + a * dt * (temp[-2] - temp[-1])

    t += dt
    # Optional: Ausgabe des aktuellen Simulationszeitpunkts
    # print("t =", t)


import time

def simulation_loop():
    global t
    start_real_time = time.perf_counter()  # Startzeit in Echtzeit

    while True:
        real_time_elapsed = time.perf_counter() - start_real_time  # Vergangene Echtzeit
        sim_time_elapsed = t  # Vergangene Simulationszeit

        if sim_time_elapsed < real_time_elapsed:
            update()  # Simulation aktualisieren
        else:
            time.sleep(0.001)  # Warten, um Echtzeit einzuhalten



first = True


def draw(frame):
    global first
    # Zeichne nur den aktuellen Zustand, ohne update() aufzurufen
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()

    # Erster Subplot: Darstellung als "Heatmap"
    # Damit imshow einen 2D-Array erhält, packen wir "temperatur" in eine Liste.
    im = axs[0].imshow([temperatur], cmap=color, aspect='auto', norm=norm)
    axs[0].set_title('Temperaturverlauf')
    axs[0].set_xlabel('Position entlang des Stabes')
    axs[0].set_yticks([])  # Y-Achsen-Beschriftungen ausblenden
    if first:
        cbar1 = plt.colorbar(im, ax=axs[0])
        cbar1.set_label('Temperatur (°C)')

    # Zweiter Subplot: Scatterplot
    sc = axs[1].scatter(x, temperatur, c=temperatur, cmap=color, norm=norm)
    axs[1].set_title('Temperaturverlauf')
    axs[1].set_xlabel('Position')
    axs[1].set_ylabel('Temperatur (°C)')
    axs[1].set_ylim(smallest, largest)
    if first:
        cbar2 = plt.colorbar(sc, ax=axs[1])
        cbar2.set_label('Temperatur (°C)')
        first = False

    # Dritter Subplot: Temperatur an einer festen Position (hier Index 100) über die Zeit
    time_data.append(t)
    temperatur_data.append(temperatur[0])
    axs[2].plot(time_data, temperatur_data, color='red')
    axs[2].set_title("Temperatur vs. Zeit")
    axs[2].set_xlabel("Zeit")
    axs[2].set_ylabel("Temperatur (K)")

    plt.tight_layout()


def asd():
    setup('inferno', 200, 0.0261, 0.01)


# Hotkeys: Mit "space" wird asd() erneut aufgerufen, mit "ctrl" beendet sich das Programm.
keyboard.add_hotkey("space", lambda: asd())
keyboard.add_hotkey("ctrl", lambda: quit(0))

# Initiale Setup-Aufrufe
asd()

# Starte die Simulation in einem eigenen Daemon-Thread
sim_thread = threading.Thread(target=simulation_loop, daemon=True)
sim_thread.start()

# Erstelle die Figuren und starte die Animation
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
ani = animation.FuncAnimation(fig, draw, frames=1000, interval=1, blit=False)
plt.show()
