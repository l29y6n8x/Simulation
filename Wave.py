import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

time_data = []
force_data = []
displacement_data = []
p_m = []
p_F = []
p_v = []
p_d = []

dt = 0.01
t = 0

k = 100
elast = 1000

x = 0
r = 5

def setup(particles, start_displacement, mass):
    global x
    for i in range(particles):
        p_m.append(mass)
        p_F.append(0)
        p_v.append(0)
        p_d.append(0)
    p_d[0] = start_displacement
    x = (1280-50) / particles

def update():
    p_F[0] = (p_d[1]-p_d[0]) * elast - p_d[0] * k

    for index in range(len(p_F) - 2):
        i = index + 1
        p_F[i] = (p_d[index]-p_d[i]) * elast + (p_d[i + 1]-p_d[i]) * elast - p_d[i] * k

    last = len(p_F)-1
    p_F[last] = (p_d[last-1] - p_d[last]) * elast -p_d[last] * k

    for index in range(len(p_v)):
        p_v[index] += (p_F[index] / p_m[index]) * dt

    for index in range(len(p_d)):
        p_d[index] += p_v[index] * dt #100 * np.sin(np.radians((2 * np.pi) / 0.02) * t )

setup(100, 100, 10)

while True:#def simulation(frame):
    t += dt

    update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)

    screen.fill("white")

    for i2 in range(len(p_m)):
        pygame.draw.circle(screen, (0, 0, 0), [x * (i2 + 1), 360 - p_d[i2]], r, r)
        if (i2 + 2) <= len(p_m):
            pygame.draw.line(screen, (0, 100, 255), [x * (i2 + 1), 360 - p_d[i2]], [x * (i2 + 2), 360 - p_d[i2+1]], int(r / 2))

    clock.tick(100)

    pygame.display.flip()