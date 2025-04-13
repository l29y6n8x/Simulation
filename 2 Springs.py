from time import sleep
import math
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.f2py.f2py2e import make_f2py_compile_parser

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

time_data = []
displacement_data = []
displacement2_data = []


dt = 0.1
t = 0

x_1 = 0
x_2 = 300.0

v_1 = -70
v_2 = 0

m_1 = 2000
m_2 = 2000

k_1 = 1000
k_2 = 1300

r = 10
w = r

y = 0


def rk_4():
    global x_1, x_2 , v_1, v_2

    k1_x_1 = v_1
    k1_v_1 = (-k_1 * x_1 + k_2 * (x_2 - x_1)) / m_1

    k1_x_2 = v_2
    k1_v_2 = (-k_2 * (x_2 - x_1)) / m_2


    k2_x_1 = v_1 + k1_v_1 * dt/2
    k2_v_1 = (-k_1 * (x_1 + k1_x_1 * dt/2) + k_2 * ((x_2 + k1_x_2 * dt/2) - (x_1 + k1_x_1 * dt/2))) / m_1

    k2_x_2 = v_2 + k1_v_2 * dt/2
    k2_v_2 = (-k_2 * ((x_2 + k1_x_2 * dt/2) - (x_1 + k1_x_1 * dt/2))) / m_2


    k3_x_1 = v_1 + k2_v_1 * dt/2
    k3_v_1 = (-k_1 * (x_1 + k2_x_1 * dt/2) + k_2 * ((x_2 + k2_x_2 * dt/2) - (x_1 + k2_x_1 * dt/2))) / m_1

    k3_x_2 = v_2 + k2_v_2 * dt/2
    k3_v_2 = (-k_2 * ((x_2 + k2_x_2 * dt/2) - (x_1 + k2_x_1 * dt/2))) / m_2


    k4_x_1 = v_1 + k3_v_1 * dt
    k4_v_1 = (-k_1 * (x_1 + k3_x_1 * dt) + k_2 * ((x_2 + k3_x_2 * dt) - (x_1 + k3_x_1 * dt))) / m_1

    k4_x_2 = v_2 + k3_v_2 * dt
    k4_v_2 = (-k_2 * ((x_2 + k3_x_2 * dt) - (x_1 + k3_x_1 * dt))) / m_2


    x_1 += (k1_x_1 + 2 * k2_x_1 + 2 * k3_x_1 + k4_x_1) * dt / 6
    v_1 += (k1_v_1 + 2 * k2_v_1 + 2 * k3_v_1 + k4_v_1) * dt / 6

    x_2 += (k1_x_2 + 2 * k2_x_2 + 2 * k3_x_2 + k4_x_2) * dt / 6
    v_2 += (k1_v_2 + 2 * k2_v_2 + 2 * k3_v_2 + k4_v_2) * dt / 6




def graph(frames):
    global t, s
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    rk_4()

    time_data.append(t)
    displacement_data.append(x_1)
    ax1.clear()
    ax1.plot(time_data, displacement_data, color='blue')
    ax1.set_title("Displacement vs Time")
    ax1.set_xlabel("")
    ax1.set_ylabel("Displacement (m)")

    displacement2_data.append(x_2)
    ax2.clear()
    ax2.plot(time_data, displacement2_data, color='blue')
    ax2.set_title("Displacement vs Time")
    ax2.set_xlabel("")
    ax2.set_ylabel("Displacement (m)")


    dx_1 = 640 - x_1
    dx_2 = 640 - x_2
    dy = 360 - y


    pygame.draw.rect(screen, ( 0, 0, 0), (dx_1 - r,dy - r, 2 * r, 2 * r))
    pygame.draw.rect(screen, (0, 0, 0), (dx_2 - r, dy - r, 2 * r, 2 * r))

    pygame.draw.line(screen, (98, 71, 51), [0, 360], [dx_1, dy], 5)
    pygame.draw.line(screen, (98, 71, 51), [dx_1, 360], [dx_2, dy], 5)
    pygame.draw.line(screen, (0, 0, 0), [0, dy + r/2 + 5], [1280, dy + r/2 + 5], 5)

    # flip() the display to put your work on screen
    pygame.display.flip()
    #sleep(dt/3.5)

    return

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

ani = animation.FuncAnimation(fig, graph, frames=1000, interval=dt , blit=False)
plt.show()

pygame.quit()