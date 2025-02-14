import math
from symtable import Symbol

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame


width = 1280
height = 720

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
y = -100
x2 = 20
y2 = 20

vx = 0
vy = 0
vx2 = 0
vy2 = 0

Fx = 0
Fy = 0
Fx2 = 0
Fy2 = 0
dx = x2 - x
dy = y2 - y
dx2 = x - x2
dy2 = y - y2

def distance(x1, y1, x2_, y2_):
    return math.sqrt(((x1 - x2_) ** 2) + ((y1 - y2_) ** 2))

d = distance(x, y, x2, y2)

def touch(x, y, x2, y2):
    return (r * 2)>= distance(x, y, x2, y2)

def momentum():
    global vx, vx2, vy, vy2
    asd = vx
    vx = vx2
    vx2 = asd

    sdf = vy
    vy = vy2
    vy2 = sdf


def force():
    global Fx, Fx2, Fy, Fy2
    angle = math.asin(dy/d)
    Fx = math.cos(angle) * (dx/abs(dx)) * G * m * m / d ** 2
    Fx2 = math.cos(angle) * (dx2/abs(dx2)) * G * m * m / d ** 2

    Fy = math.sin(angle) * (dy/abs(dy)) * G * m * m / d ** 2
    Fy2 = math.sin(angle) * (dy2/abs(dy2)) * G * m * m / d ** 2

def velocity():
    global vx, vx2, vy, vy2
    if touch(x, y, x2, y2):
        momentum()
    else:
        vx += Fx/m * dt
        vx2 += Fx2 / m * dt

        vy += Fy/m * dt
        vy2 += Fy2 / m * dt

def position():
    global dx, x, x2, dx2, d, dy, y, y2, dy2
    x += vx * dt
    x2 += vx2 * dt

    y += vy * dt
    y2 += vy2 * dt

    dx = x2 - x
    dx2 = x - x2
    dy = y2 - y
    dy2 = y - y2
    d = distance(x, y, x2, y2)


while True: #def simulation(frame):
    #global t
    #t += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    force()
    velocity()
    position()


    screen.fill("white")

    pygame.draw.circle(screen, (0, 0, 0), [int(640 + x), int(360 + y)], r)
    pygame.draw.circle(screen, (0, 0, 0), [int(640 + x2), int(360 + y2)], r)

    clock.tick(100)

    pygame.display.flip()

    time_data.append(t)

    #force_data.append(Fx)
    #displacement_data.append(x)
    #ax1.clear()
    #ax1.plot(time_data, force_data, color='blue')
    #ax1.set_title("Force vs Time")
    #ax1.set_xlabel("")
    #ax1.set_ylabel("Force (F)")
    #ax2.clear()
    #ax2.plot(time_data, displacement_data, color='blue')
    #ax2.set_title("Displacement vs Time")
    #ax2.set_xlabel("")
    #ax2.set_ylabel("Displacement (cm)")
    #return

#fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
#
#ani = animation.FuncAnimation(fig, simulation, frames=1000, interval=dt * 1000, blit=False)
#plt.show()