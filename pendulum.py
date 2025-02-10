from time import sleep
import math
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pygame import Vector2

def dichte():
    Aerogel = 3


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

time_data = []
force_data = []
displacement_data = []

dt = 0.01
t = 0


l = 300 # cm
SIl = l/100 # m
s = 19# (alpha / 360) * 2 * math.pi * l * 0.01  # cm
SIs = s/100
alpha = (SIs * 360) / ( 2 * math.pi * SIl)

v = 0 # m/s
F = 0 # N

r = 30 # cm
SIr = r / 100  # m
w = r

p = 0.03 # kg/m**3
m = p * 4/3 * math.pi * SIr ** 3 # kg
pl = 1.225 # kg/m**3
g = 9.81 # m/s**2
Fg = m * g # N
print(m)

Cw = 0.45
A = 0.5 * math.pi * SIr ** 2 # m**2


x = 0
y = 0

w = int(w)
s = float(s)

def force():
    global F
    F = math.sin(alpha) * Fg  # Use radians for math.sin


def velocity():

    global dt, v, F, m
    if v > 0:
        v = v + (F - 0.5 * A * pl * Cw * v ** 2) / m * dt
    elif v < 0:
        v = v + (F + 0.5 * A * pl * Cw * v ** 2) / m * dt
    else:
        v = v + F / m * dt

def displacement():
    global SIs, alpha
    SIs = SIs + v * dt
    alpha = (SIs * 360) / (2 * math.pi * SIl)

def sim(frames):
    global x, y, t
    t += dt

    force()
    velocity()
    displacement()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    x = 640 + math.sin(alpha) * l
    y = 300 - math.cos(alpha) * l

    pygame.draw.circle(screen, (0, 0, 0), [x, y], r, w)
    pygame.draw.line(screen, (98, 71, 51), [640, 300], [x, y], 5)

    pygame.display.flip()

    time_data.append(t)
    force_data.append(F)
    displacement_data.append(SIs)
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

ani = animation.FuncAnimation(fig, sim, frames=1000, interval=dt * 1000, blit=False)
plt.show()

pygame.quit()