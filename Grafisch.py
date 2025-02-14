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

pi = math.pi

class Material:
    luft = 1.225
    aerogel = 150
    christkugel = 159.95
    eis = 917
    fichtenholz = 420
    glas = 2500
    eisen = 7850
    gold = 19300

dt = 0.01
t = 0

l = 300 # cm
SIl = l/1000 # m
alpha = 100
s = (alpha / 360) * 2 * math.pi * SIl # m
#alpha = (s * 360) / ( 2 * math.pi * SIl)


r = 32.5 # cm
SIr = r / 1000  # m
w = r
w = int(w)

v = 5 # m/s
F = 0 # N

pl = 1.225 # kg/m**3
p = Material.eisen # kg/m**3
Cw = 0.45
A = 0.5 * math.pi * SIr ** 2 # m**2

m = p * 4/3 * math.pi * SIr ** 3 # kg
g = 9.81 # m/s**2
Fg = m * g # N
print(m)

def force():
    global F
    F = -math.sin(math.radians(alpha)) * Fg

def velocity():

    global dt, v, F, m
    if v < 0:
        v += (F + 0.5 * A * pl * Cw * v ** 2) / m * dt
    elif v > 0:
        v += (F - 0.5 * A * pl * Cw * v ** 2) / m * dt
    else:
        v += F / m * dt

def displacement():
    global s, alpha
    s = s + v * dt
    alpha += (v * dt * 360) / (2 * math.pi * SIl)



def sim(frames):
    global t
    t += dt

    #Berechnung

    force()
    velocity()
    displacement()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    x = 640 + math.sin(math.radians(alpha)) * l
    y = 300 + math.cos(math.radians(alpha)) * l

    fx = x + math.sin(math.radians(alpha + 90)) * F * 10
    fy = y + math.cos(math.radians(alpha + 90)) * F * 10

    pygame.draw.circle(screen, (0, 0, 0), [x, y], r, w)
    pygame.draw.line(screen, (98, 71, 51), [640, 300], [x, y], 5)
    pygame.draw.line(screen, (255, 0, 0), [x, y], [fx, fy], 5)

    pygame.display.flip()

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
    ax2.set_ylabel("Displacement (cm)")

    # sleep(1)

    return

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

ani = animation.FuncAnimation(fig, sim, frames=1000, interval=dt * 1000, blit=False)
plt.show()

pygame.quit()