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

dt = 0.1
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


def displacement():
    global s, v
    s = 200 * math.cos(math.radians(math.sqrt(5) * t))#s = s + v * dt

def graph(frame):
    global t, s
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    displacement()

    time_data.append(t)
    displacement_data.append(s)
    ax1.clear()
    ax1.plot(time_data, displacement_data, color='blue')
    ax1.set_title("Displacement vs Time")
    ax1.set_xlabel("")
    ax1.set_ylabel("Displacement (m)")


    dx = 640 - s
    dy = 360 - y
    pygame.draw.rect(screen, ( 0, 0, 0), (dx-r,dy-r, 2 * r, 2 * r)) # Rect(left, top, width, height) -> Rect
    pygame.draw.line(screen, (98, 71, 51), [0, 360], [dx, dy], 5)
    pygame.draw.line(screen, (0, 0, 0), [0, dy + r/2 + 5], [1280, dy + r/2 + 5], 5)

    # flip() the display to put your work on screen
    pygame.display.flip()

    return

fig, (ax1) = plt.subplots(1, 1, figsize=(6, 8))

ani = animation.FuncAnimation(fig, graph, frames=1000, interval=dt , blit=False)
plt.show()

pygame.quit()