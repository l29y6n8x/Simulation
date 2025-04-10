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
displacement_data = []
displacement2_data = []
error_data = []

dt = 0.1
t = 0

s = 200.0
s2 = 200.0
s3 = 200.0
v = 0
v2 = 0
F = 0
F2 = 0

m = 200
k = 1000

r = 10
w = r

x = 0
y = 0

s = float(s)

def rk_4():
    global v, s2

    kv1 = -k * s2 / m
    kx1 = v

    kv2 = -k * (s2 + kx1 * dt / 2 ) / m
    kx2 = v + kv1 * dt / 2

    kv3 = -k * (s2 + kx2 * dt / 2) / m
    kx3 = v + kv2 * dt / 2

    kv4 = -k * (s2 + kx3 * dt) / m
    kx4 = v + kv3 * dt

    v += (kv1 + 2 * kv2 + 2 * kv3 + kv4) * dt / 6
    s2 += (kx1 + 2 * kx2 + 2 * kx3 + kx4) * dt / 6



def displacement():
    global s, s3, v2
    s = 200 * math.cos(math.sqrt(k/m) * t)#s = s + v * dt
    v2 += -k * s3 / m * dt
    s3 += v2 * dt

def graph(frame):
    global t, s
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    displacement()
    rk_4()

    time_data.append(t)
    displacement_data.append(s)
    ax1.clear()
    ax1.plot(time_data, displacement_data, color='blue')
    ax1.set_title("Displacement vs Time")
    ax1.set_xlabel("")
    ax1.set_ylabel("Displacement (m)")

    displacement2_data.append(s2)
    ax2.clear()
    ax2.plot(time_data, displacement2_data, color='blue')
    ax2.set_title("Displacement vs Time")
    ax2.set_xlabel("")
    ax2.set_ylabel("Displacement (m)")

    error_data.append(s3)#s-s2
    ax3.clear()
    ax3.plot(time_data, error_data, color='blue')
    ax3.set_title("Error vs Time")
    ax3.set_xlabel("")
    ax3.set_ylabel("Error (m)")



    dx = 640 - s
    dy = 360 - y

    dx2 = 640 - s2
    dy2 = 500 - y

    dx3 = 640 - s3
    dy3 = 640 - y

    pygame.draw.rect(screen, ( 0, 0, 0), (dx-r,dy-r, 2 * r, 2 * r)) # Rect(left, top, width, height) -> Rect
    pygame.draw.line(screen, (98, 71, 51), [0, 360], [dx, dy], 5)
    pygame.draw.line(screen, (0, 0, 0), [0, dy + r/2 + 5], [1280, dy + r/2 + 5], 5)

    pygame.draw.line(screen, (98, 71, 51), [0, 500], [dx2, dy2], 5)
    pygame.draw.rect(screen, (0, 0, 0), (dx2 - r, dy2 - r, 2 * r, 2 * r))

    pygame.draw.line(screen, (98, 71, 51), [0, 640], [dx3, dy3], 5)
    pygame.draw.rect(screen, (0, 0, 0), (dx3 - r, dy3 - r, 2 * r, 2 * r))

    # flip() the display to put your work on screen
    pygame.display.flip()
    #sleep(dt/3.5)

    return

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))

ani = animation.FuncAnimation(fig, graph, frames=1000, interval=dt , blit=False)
plt.show()

pygame.quit()