import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import numpy as np
from perlin_noise import PerlinNoise

temperature, fig, axs, xCord, yCord, old_temp, dt, t = [], 0, [], 0, 0, [], 0, 0
temperature_data = []
time_data = []

def setup(size, time_interval, heat_conductivity):
    global temperature, fig, axs, xCord, yCord, dt, a
    dt = time_interval
    a = heat_conductivity
    noise = PerlinNoise(octaves=2)
    xCord, yCord = size, int(size / 5)


    temperature = [[10 * noise([i / xCord, j / yCord]) for j in range(xCord)] for i in range(yCord)]
    fig, axs = plt.subplots(2, 1, figsize=(10, 4), layout='constrained')

    sum_T = 0
    for i in range(yCord):
        for j in range(xCord):
            sum_T = sum_T + temperature[i][j]
    start_avrg_temp = sum_T/ (yCord * xCord)

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

    diff = add/asd - old_temp[y][x]

    return diff

def get_temp_diff(x, y, diff):
    temperature[y][x] = old_temp[y][x] + a * diff * dt

def get_avrg_temp():
    sum_T = 0
    for i in range(yCord):
        for j in range(xCord):
            sum_T = sum_T + temperature[i][j]
    return sum_T/ (yCord * xCord)

def update(frame):
    global old_temp
    old_temp = temperature.copy()

    for i in range(yCord):
        for j in range(xCord):
            diff = get_next_values(j, i, len(temperature[0])-1, len(temperature)-1)
            get_temp_diff(j, i, diff)
    draw()


first = True

def draw():
    global first, t
    t += dt
    psm = axs[0].pcolormesh(temperature, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
    if first:
        cbar = fig.colorbar(psm, ax=axs[0])
        cbar.set_label('Temperatur (K)')
        first = False
    time_data.append(t)
    temperature_data.append(get_avrg_temp())
    gra = axs[1].plot(time_data, temperature_data, color='red')


cmap = 'inferno'
setup(200, 0.01, 80.2)

ani = animation.FuncAnimation(fig, update, frames=1000, interval=1, blit=False)
plt.show()