import math
import random
import pygame

dt = 0.01
G = 6.67430 * 10 ** -11

ds = 0.0

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

m = []
vx = []
vy = []
Fx = []
Fy = []
px = []
py = []
dx = []
dy = []

r = 5

def distance(x, y, x2, y2):
    d = math.sqrt(((x - x2) * (x - x2)) + ((y - y2) * (y - y2)))
    return d

def random_():
    h = random.randrange(0, height)
    w = random.randrange(0, width)
    return w, h

def is_near(spacing, x, y):
    for i in range(len(px)):
        x2 = px[i]
        y2 = py[i]
        if distance(x, y, x2 ,y2) < spacing:
            return True
    return False

def new_random_location(spacing):
    if len(px) == 0:
        return random_()
    else:
        x, y = random_()
        if not is_near(spacing, x, y):
            return x, y
        else:
            return new_random_location(spacing)

def setup(particles, spacing, mass):
    for index in range(particles):
        x, y = new_random_location(spacing)
        m.append(mass)
        vx.append(0)
        vy.append(0)
        Fx.append(0)
        Fy.append(0)
        px.append(x)
        py.append(y)
        dx.append(0)
        dy.append(0)

def force():
    global ds
    for i in range(len(Fx)):
        distances = []
        for index in range(len(Fx)-1):
            dx[index] = px[index] - px[index + 1]
            distances.append(distance(px[i], py[i], px[index + 1], py[index + 1]))

        for index in range(len(Fx)-1):
            dy[index] = py[index] - py[index + 1]

        ds = math.sqrt(dx[i] ** 2 + dy[i] ** 2)
        Fx[i] = G * (m[i] * m[i + 1]) / ds ** 2

setup(2, 100, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                m.clear()
                vx.clear()
                vy.clear()
                Fx.clear()
                Fy.clear()
                px.clear()
                py.clear()
                dx.clear()
                dy.clear()
                setup(2, 100, 100)

    screen.fill("white")

    for ip in range(len(px)):
        pygame.draw.circle(screen, (0, 0, 0), [px[ip], py[ip]], r, r)
        pygame.draw.circle(screen, (0, 0, 0), [px[ip], py[ip]], 100, r)

    clock.tick(100)
    pygame.display.flip()

pygame.quit()