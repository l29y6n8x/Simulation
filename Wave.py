import pygame

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

time_data = []
force_data = []
displacement_data = []

dt = 0.01
t = 0

k = 100
elast = 100

particles = []

class Particle:
    def __init__(self, x, y, r, amount):
        self.y = y
        self.x = x
        self.r = r#
        self.m = 100
        self.amount = amount
        self.F = 0
        self.v = 0
        self.dy = 0

    def delta_y(self, i):
        if i == 0:
            self.dy = (particles[i+1].y - self.y)
        elif i == self.amount-1:
            self.dy = (particles[i-1].y - self.y)
        else:
            self.dy = (particles[i+1].y + particles[i-1].y) / 2 - self.y

    def force(self):
        self.F = self.dy * elast

    def velocity(self):
        self.v += self.F / self.m * dt

    def position(self):
        self.y += self.v * dt

    def draw(self, i, points, lines):
        if points:
            pygame.draw.circle(screen, (0, 0, 0), [self.x, self.y], self.r, self.r)
        if lines:
            if i != self.amount-1:
                other = particles[i+1]
                pygame.draw.line(screen, (0, 64, 128), [self.x, self.y], [other.x, other.y], 2)

def setup():
    amount = 100
    for i in range(amount):
        pos = i * (width/amount) + (width/amount) / 2
        par = Particle(pos, height/2, 5, amount)
        particles.append(par)
    particles[int(amount/2)].y = 200

def update():
    for i, particle in enumerate(particles):
        particle.delta_y(i)
        particle.force()
        particle.velocity()
        particle.position()
        particle.draw(i, True, True)


while True:
    t += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                particles.clear()
                setup()

    screen.fill("white")

    update()

    clock.tick(100)

    pygame.display.flip()