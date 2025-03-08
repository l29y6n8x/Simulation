import random
import keyboard
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
        rand = 20 * np.cos((np.pi * 2 * 3 / r) * i)#random.randrange(-60, 61) / 10 + last
        randoms.append(rand)
        last = rand
    return randoms

def getBig(list):
    big = 0
    for i in range(len(list)):
        if list[i] > list[big]:
            big = i
    return list[big]

def getSmall(list):
    small = 0
    for i in range(len(list)):
        if list[i] < list[small]:
            small = i
    return list[small]

def setup(colormap, resulution, Temperaturleitfaehigkeit, Zeitintervall):
    global axs, temp_array, temperatur, norm, x, color, r, a, dt, fig, smallest, largest
    color = colormap
    r = resulution
    a = Temperaturleitfaehigkeit
    dt = Zeitintervall

    randoms = temps(r)
    temperatur = np.array([randoms[i] for i in range(r)])
    print(len(temperatur))
    temp_array = [temperatur]
    x = np.linspace(0, 10, r)

    # Normalisiere die Temperaturwerte für den Scatterplot
    norm = mcolors.Normalize(vmin=temperatur.min(), vmax=temperatur.max())
    largest = getBig(temperatur)
    smallest = getSmall(temperatur)


def update():
    global temperatur, norm, temp_array, t
    temp = temperatur.copy()

    # Vektorisierte Berechnung (kein explizites Loopen über jeden Punkt)
    for i in range(r-1):
        temperatur[i] += a * dt * ((temp[i-1] + temp[i+1]) / 2 - temp[i])

    # Randbedingungen korrigieren
    temperatur[0] = temp[0] + a * dt * (temp[1] - temp[0])
    temperatur[-1] = temp[-1] + a * dt * (temp[-2] - temp[-1])

    temp_array = [temperatur]
    t += dt
    print(t)


first = True

def draw(frame):
    global first
    # --- Erster Subplot: Farbbalken mit imshow ---
    update()
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    im = axs[0].imshow(temp_array, cmap=color, aspect='auto', norm=norm)
    axs[0].set_title('Temperaturverlauf')
    axs[0].set_xlabel('Position entlang des Stabes')
    axs[0].set_yticks([])  # Entferne y-Achsen-Beschriftungen
    if first:
        cbar1 = plt.colorbar(im, ax=axs[0])
        cbar1.set_label('Temperatur (°C)')

    # --- Zweiter Subplot: Scatterplot ---

    sc = axs[1].scatter(x, temperatur, c=temperatur, cmap=color, norm=norm)
    axs[1].set_title('Temperaturverlauf')
    axs[1].set_xlabel('Position')
    axs[1].set_ylabel('Temperatur (°C)')
    axs[1].set_ylim(smallest, largest)
    if first:
        cbar2 = plt.colorbar(sc, ax=axs[1])
        cbar2.set_label('Temperatur (°C)')
        first = False

    time_data.append(t)
    temperatur_data.append(temperatur[100])
    axs[2].plot(time_data, temperatur_data, color='red')
    axs[2].set_title("Temperatur vs Time")
    axs[2].set_xlabel("")
    axs[2].set_ylabel("Temperatur (K)")

    plt.tight_layout()


def asd():
    setup('inferno', 200, 80.2, 0.01)

keyboard.add_hotkey("space", lambda: asd())

keyboard.add_hotkey("ctrl", lambda: quit(0))


asd()
#while True:
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
ani = animation.FuncAnimation(fig, draw, frames=1000, interval=1, blit=False)
plt.show()
