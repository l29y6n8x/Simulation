import random
import pygame

dt = 0.001
t = 0
G = 6.67430 * 10 ** -11

elastic = 0.95

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

global_amount = 0
global_spacing = 0
global_mass = 0

particles = []

class Particle:
    def __init__(self, x, y, mass, radius=10):
        global particles
        self.p = pygame.math.Vector2(x, y)
        self.F = pygame.math.Vector2(0, 0)
        self.v = pygame.math.Vector2(0, 0)
        self.m = mass
        self.r = radius
        particles.append(self)
        self.draw()

    def force(self):
        self.F = pygame.math.Vector2(0, 0)
        for particle in particles:
            if particle != self:
                displacement = particle.p - self.p
                distance = displacement.length()
                if distance == 0:
                    continue
                force_magnitude = G * self.m * particle.m / (distance ** 2)
                self.F += displacement.normalize() * force_magnitude



    def velocity(self):

        if self.p.x - self.r <= 0 or self.p.x + self.r >= width:
            self.v.x *= -elastic
        if self.p.y - self.r <= 0 or self.p.y + self.r >= height:
            self.v.y *= -elastic



        self.v += self.F * (1 / self.m) * dt

    def position(self):
        for particle in particles:
            if particle != self:
                if (self.r + particle.r) >= self.p.distance_to(particle.p):
                    self.collide(particle)
                    print(True)

        self.p += self.v * dt

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), self.p, self.r, self.r)

    def distance(self, other):
        return self.p.distance_to(other)

    def collide(self, other):
        impulse = self.v * self.m
        impulse2 = other.v * other.m

        self.v = elastic * impulse2 / self.m
        other.v = elastic * impulse / other.m

def update():
    for particle in particles:
        particle.force()

    #for i in range(len(particles)):
    #    for j in range(i + 1, len(particles)):
    #        p1 = particles[i]
    #        p2 = particles[j]
#
    #        if (p1.r + p2.r) >= p1.p.distance_to(p2.p):
    #            p1.collide(p2)
    #            print(True)

    for particle in particles:
        particle.velocity()
        particle.position()
        particle.draw()


def random_():
    h = random.randrange(0, height)
    w = random.randrange(0, width)
    return w, h

def is_near(spacing, x3, y3):
    for particle in particles:
        if particle.distance(pygame.math.Vector2(x3, y3)) < spacing:
            return True
    return False

def new_random_location(spacing):
    if len(particles) == 0:
        return random_()
    else:
        x2, y2 = random_()
        if not is_near(spacing, x2, y2):
            return x2, y2
        else:
            return new_random_location(spacing)

def setup(amount, spacing, mass):
    global global_amount, global_mass, global_spacing
    global_mass = mass
    global_spacing = spacing
    global_amount = amount
    for index in range(amount):
        x, y = new_random_location(spacing)
        Particle(x, y, mass)

def reset():
    setup(global_amount, global_spacing, global_mass)

setup(30, 100, 1e17)

while running:
    t += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                particles.clear()
                reset()

    screen.fill("white")

    update()

    clock.tick(50)
    pygame.display.flip()

pygame.quit()