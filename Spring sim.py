from time import sleep
import math
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

time_data = []
force_data = []
displacement_data = []

dt = 0.01
sdt = 0.01
t = 0

s = 200.0
v = 0
F = 0

m = 200
k = 1000
µ = 0.3
g = 9.81
Fg = m * g

r = 10
w = r

x = 0
y = 0

s = float(s)

def force():
    global F, k, s
    F = -s * k

def velocity():
    global dt, v, F, m
    if v > 0:
        v = v + (F - Fg * µ) / m * dt
    elif v < 0:
        v = v + (F + Fg * µ) / m * dt
    else:
        v = v + F / m * dt

def displacement():
    global sdt, s, v
    s = s + v * sdt

def graph(frame):
    global t, s
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    force()
    velocity()
    displacement()

    time_data.append(t)
    force_data.append(F)
    displacement_data.append(s)
    ax1.clear()
    ax1.plot(time_data, force_data, color='blue')
    ax1.set_title("Force vs Time")
    ax1.set_xlabel("")
    ax1.set_ylabel("Force (F)")
    ax2.clear()
    ax2.plot(time_data, displacement_data, color='blue')
    ax2.set_title("Displacement vs Time")
    ax2.set_xlabel("")
    ax2.set_ylabel("Displacement (m)")


    dx = 640 - s
    dy = 360 - y
    pygame.draw.rect(screen, ( 0, 0, 0), (dx-r,dy-r, 2 * r, 2 * r)) # Rect(left, top, width, height) -> Rect
    pygame.draw.line(screen, (98, 71, 51), [0, 360], [dx, dy], 5)
    pygame.draw.line(screen, (0, 0, 0), [0, dy + r/2 + 5], [1280, dy + r/2 + 5], 5)

    # flip() the display to put your work on screen
    pygame.display.flip()

    return

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

ani = animation.FuncAnimation(fig, graph, frames=1000, interval=dt * 1000, blit=False)
plt.show()

pygame.quit()