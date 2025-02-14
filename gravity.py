import math
import random
import pygame

dt = 0.01
G = 6.67430 * 10 ** -11

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
x = []
y = []
dx = []
dy = []
d = []

r = 5

def last(array, index):
    return index == len(array)-1

def distance(x, y, x2, y2):
    return math.sqrt(((x - x2) * (x - x2)) + ((y - y2) * (y - y2)))

def random_():
    h = random.randrange(0, height)
    w = random.randrange(0, width)
    return w, h

def is_near(spacing, x3, y3):
    for i in range(len(x)):
        x2 = x[i]
        y2 = y[i]
        if distance(x3, y3, x2 ,y2) < spacing:
            return True
    return False

def new_random_location(spacing):
    if len(x) == 0:
        return random_()
    else:
        x2, y2 = random_()
        if not is_near(spacing, x2, y2):
            return x2, y2
        else:
            return new_random_location(spacing)

def setup(particles, spacing, mass):
    for index in range(particles):
        xn, yn = new_random_location(spacing)
        m.append(mass)
        vx.append(0)
        vy.append(0)
        Fx.append(0)
        Fy.append(0)
        x.append(xn)
        y.append(yn)
        dx.append(0)
        dy.append(0)
        d.append(0)

    dx[0] = x[1] - x[0]
    dy[0] = y[1] - y[0]
    dx[1] = x[0] - x[1]
    dy[1] = y[0] - y[1]
    d[0] = distance(x[0], y[0], x[1], y[1])
    d[1] = distance(x[0], y[0], x[1], y[1])


def touch(x, y, x2, y2):
    return (r * 2)>= distance(x, y, x2, y2)

def collide(index, index2):
    global vx, vy

    mvx = vx[index]
    vx[index] = vx[index2]
    vx[index2] = mvx

    my = vy[index]
    vy[index] = vy[index2]
    vy[index2] = my


def force():
    global Fx, Fy
    print(Fy)
    for i in range(len(m)):
        angle = math.asin(dy[i]/d[i])
        Fx[i] = math.cos(angle) * (dx[i]/abs(dx[i])) * G * m[i] * m[i] / d[i] ** 2

        Fy[i] = math.sin(angle) * G * m[i] * m[i] / d[i] ** 2

def velocity():
    global vx, vy
    for i in range(len(m)):
        if touch(x[0], y[0], x[1], y[1]):
            if not last(m, i):
                collide(i, i+1)
        else:
            vx[i] += Fx[i]/m[i] * dt
            vy[i] += Fy[i]/m[i] * dt

def position():
    global dx, x, d, dy, y
    for i in range(len(m)):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
        #buildx = []
        #for i2 in range(len(m)):
        #    buildx.append(distance())
        #    dx[i] = x[i+1] - x[i]
        #    dy[i] = y[i+1] - y[i]
    dx[0] = x[1] - x[0]
    dy[0] = y[1] - y[0]
    dx[1] = x[0] - x[1]
    dy[1] = y[0] - y[1]
    d[0] = distance(x[0], y[0], x[1], y[1])
    d[1] = distance(x[0], y[0], x[1], y[1])

setup(2, 100, 1000000000000000)

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
                x.clear()
                y.clear()
                dx.clear()
                dy.clear()
                setup(2, 100, 1000000000000000)

    force()
    velocity()
    position()

    screen.fill("white")

    for ip in range(len(m)):
        pygame.draw.circle(screen, (0, 0, 0), [x[ip], y[ip]], r, r)
        #pygame.draw.circle(screen, (0, 0, 0), [x[ip], y[ip]], 100, r)

    #clock.tick(144)
    pygame.display.flip()

pygame.quit()