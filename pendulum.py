import math
from symtable import Symbol

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame


width = 1280
height = 720

last = 0

r = 10

t = 0

time_data = []
force_data = []
displacement_data = []

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

dt = 0.01
G = 6.67430 * 10 ** -11

m = 1000000000000000
x = -20
x2 = 20
v = 0
v2 = 0
F = 0
F2 = 0
d = x2 - x
d2 = x - x2

def distance(x1, y1, x2_, y2_):
    return math.sqrt(((x1 - x2_) * (x1 - x2_)) + ((y1 - y2_) * (y1 - y2_)))

def touch(x, y, x2, y2):
    return (r * 2)>= distance(x, y, x2, y2)

def momentum():
    global v, v2
    asd = v
    v = v2
    v2 = asd


def force():
    global F, F2
    F = (d/abs(d)) * G * m * m / d ** 2
    F2 = (d2/abs(d2)) * G * m * m / d2 ** 2


def velocity():
    global v, v2
    if touch(x, 0, x2, 0):
        momentum()
    else:
        v += F/m * dt
        v2 += F2 / m * dt

def position():
    global d, x, x2, last, d2
    x += v * dt
    x2 += v2 * dt
    d = x2 - x
    d2 = x - x2



def simulation(frame):
    global t
    t += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    force()
    velocity()
    position()


    screen.fill("white")

    pygame.draw.circle(screen, (0, 0, 0), [int(640 + x), 360], r)
    pygame.draw.circle(screen, (0, 0, 0), [int(640 + x2), 360], r)

    clock.tick(100)

    pygame.display.flip()

    time_data.append(t)
    force_data.append(v)
    displacement_data.append(x)
    ax1.clear()
    ax1.plot(time_data, force_data, color='blue')
    ax1.set_title("Force vs Time")
    ax1.set_xlabel("")
    ax1.set_ylabel("Force (F)")
    ax2.clear()
    ax2.plot(time_data, displacement_data, color='blue')
    ax2.set_title("Displacement vs Time")
    ax2.set_xlabel("")
    ax2.set_ylabel("Displacement (cm)")

    # sleep(1)

    return

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

ani = animation.FuncAnimation(fig, simulation, frames=1000, interval=dt * 1000, blit=False)
plt.show()