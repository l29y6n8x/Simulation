import math
import random
import pygame

# Konstanten
dt = 0.01
G = 6.67430e-11

width, height = 1280, 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# Partikel-Listen
m, vx, vy, Fx, Fy, x, y = [], [], [], [], [], [], []
dx, dy, d = [], [], []

r = 5  # Partikelradius


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def random_position():
    return random.randrange(0, width), random.randrange(0, height)


def is_near(spacing, x3, y3):
    return any(distance(x3, y3, x[i], y[i]) < spacing for i in range(len(x)))


def new_random_location(spacing):
    while True:
        x2, y2 = random_position()
        if not is_near(spacing, x2, y2):
            return x2, y2


def setup(particles, spacing, mass):
    global m, vx, vy, Fx, Fy, x, y, dx, dy, d
    m.clear(), vx.clear(), vy.clear(), Fx.clear(), Fy.clear()
    x.clear(), y.clear(), dx.clear(), dy.clear(), d.clear()
    for _ in range(particles):
        xn, yn = new_random_location(spacing)
        m.append(mass)
        vx.append(0)
        vy.append(0)
        Fx.append(0)
        Fy.append(0)
        x.append(xn)
        y.append(yn)
        dx.append([])
        dy.append([])
        d.append([])


def update_forces():
    global Fx, Fy
    Fx = [0] * len(m)
    Fy = [0] * len(m)
    for i in range(len(m)):
        for j in range(len(m)):
            if i != j:
                dx_ij = x[j] - x[i]
                dy_ij = y[j] - y[i]
                d_ij = distance(x[i], y[i], x[j], y[j])
                if d_ij > 0:
                    F = G * m[i] * m[j] / d_ij ** 2
                    angle = math.atan2(dy_ij, dx_ij)
                    Fx[i] += math.cos(angle) * F
                    Fy[i] += math.sin(angle) * F


def update_velocity():
    for i in range(len(m)):
        vx[i] += (Fx[i] / m[i]) * dt
        vy[i] += (Fy[i] / m[i]) * dt


def update_positions():
    for i in range(len(m)):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt


def handle_collisions():
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            if distance(x[i], y[i], x[j], y[j]) < r * 2:
                vx[i], vx[j] = vx[j], vx[i]
                vy[i], vy[j] = vy[j], vy[i]


setup(5, 100, 1e15)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            setup(5, 100, 1e15)

    update_forces()
    update_velocity()
    update_positions()
    handle_collisions()

    screen.fill("white")
    for i in range(len(m)):
        pygame.draw.circle(screen, (0, 0, 0), (int(x[i]), int(y[i])), r)

    clock.tick(100)
    pygame.display.flip()

pygame.quit()
