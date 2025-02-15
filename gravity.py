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
    return math.sqrt(((x - x2) ** 2) + ((y - y2) ** 2))

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
    m[0] = 100000000000
    vx[0] = 0
    vy[0] = 0
    Fx[0] = 0
    Fy[0] = 0
    x[0] = 640
    y[0] = 360
    position()


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
    #print(Fx)
    for i in range(len(m)):
        for index in range(len(dx[0])):
            angle = math.asin(dy[i][index]/d[i][index])
            Fx[i] += math.cos(angle) * (dx[i][index]/abs(dx[i][index])) * G * m[i] * m[i] / d[i][index] ** 2 #  (dx[i][index]/abs(dx[i][index])) *

            Fy[i] += math.sin(angle) * G * m[i] * m[i] / d[i][index] ** 2 #  * (dy[i][index]/abs(dy[i][index]))

def velocity():
    global vx, vy
    for i in range(len(m)):
        succ = True
        for i2 in range(len(m)):
            if succ:
                if i != i2:
                    if touch(x[i], y[i], x[i2], y[i2]):
                        succ = False
                        collide(i, i2)
                        break
        if succ:
            vx[i] += Fx[i]/m[i] * dt
            vy[i] += Fy[i]/m[i] * dt

def position():
    global dx, x, d, dy, y
    for i in range(len(m)):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
    for i in range(len(m)):
        buildx = []
        for i2 in range(len(m)):
            dis = x[i2] - x[i]
            if dis != 0:
                buildx.append(dis)

        buildy = []
        for i2 in range(len(m)):
            dis = y[i2] - y[i]
            if dis != 0:
                buildy.append(dis)

        buildd = []
        for i2 in range(len(m)):
            dis = distance(x[i], y[i], x[i2], y[i2])
            if dis != 0:
                buildd.append(dis)

        dx[i] = buildx
        dy[i] = buildy
        d[i] = buildd
    #dx[0] = x[1] - x[0]
    #dy[0] = y[1] - y[0]
    #dx[1] = x[0] - x[1]
    #dy[1] = y[0] - y[1]
    #d[0] = distance(x[0], y[0], x[1], y[1])
    #d[1] = distance(x[0], y[0], x[1], y[1])

setup(10, 100, 10000000000000)

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
                setup(10, 100, 10000000000000)

    force()
    velocity()
    position()

    screen.fill("white")

    for ip in range(len(m)):
        pygame.draw.circle(screen, (0, 0, 0), [x[ip], y[ip]], r, r)
        #pygame.draw.circle(screen, (0, 0, 0), [x[ip], y[ip]], 100, r)

    clock.tick(50)
    pygame.display.flip()

pygame.quit()