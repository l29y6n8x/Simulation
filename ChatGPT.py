import random
import pygame

# Konstanten
dt = 0.01
G = 6.67430e-11  # Gravitationskonstante
width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# Liste, in der alle Partikel gespeichert werden
particles = []


class Particle:
    def __init__(self, x, y, mass, radius=5):
        # Position, Geschwindigkeit und Kraft als Vektoren
        self.p = pygame.math.Vector2(x, y)
        self.v = pygame.math.Vector2(0, 0)
        self.F = pygame.math.Vector2(0, 0)
        self.m = mass
        self.r = radius
        particles.append(self)

    def force(self):
        """Berechnet die Gravitationskraft aller anderen Partikel auf dieses Partikel."""
        self.F = pygame.math.Vector2(0, 0)
        for particle in particles:
            if particle != self:
                displacement = particle.p - self.p
                distance = displacement.length()
                if distance == 0:
                    continue  # Vermeide Division durch 0
                force_magnitude = G * self.m * particle.m / (distance ** 2)
                self.F += displacement.normalize() * force_magnitude

    def collide(self, other):
        """Berechnet und wendet den Impuls einer elastischen Kollision an."""
        # Berechne den Normalenvektor (Richtung von self zu other)
        normal = (other.p - self.p).normalize()
        # Berechne den relativen Geschwindigkeitsvektor
        relative_velocity = self.v - other.v
        # Bestimme den Anteil der relativen Geschwindigkeit in Richtung des Normals
        vel_along_normal = relative_velocity.dot(normal)

        # Wenn die Partikel sich bereits voneinander entfernen, erfolgt keine Kollision
        if vel_along_normal >= 0:
            return

        # Berechne den Impuls gemäß der Formel für einen elastischen Stoß (Restitutionskoeffizient = 1)
        impulse_scalar = -2 * vel_along_normal / (1 / self.m + 1 / other.m)
        impulse = impulse_scalar * normal

        # Aktualisiere die Geschwindigkeiten
        self.v += impulse / self.m
        other.v -= impulse / other.m

    def velocity(self):
        """Aktualisiert die Geschwindigkeit durch die wirkenden Kräfte und behandelt Wandkollisionen."""
        # Wandkollision: Bei Erreichen des Randes wird die entsprechende Komponente umgekehrt.
        if self.p.x - self.r <= 0 or self.p.x + self.r >= width:
            self.v.x *= -1
        if self.p.y - self.r <= 0 or self.p.y + self.r >= height:
            self.v.y *= -1
        # Aktualisiere die Geschwindigkeit durch den Einfluss der Kraft (F = m * a)
        self.v += (self.F / self.m) * dt

    def position(self):
        """Aktualisiert die Position basierend auf der Geschwindigkeit."""
        self.p += self.v * dt

    def draw(self):
        """Zeichnet das Partikel als Kreis."""
        pygame.draw.circle(screen, (0, 0, 0), (int(self.p.x), int(self.p.y)), self.r)


def update():
    """Aktualisiert den Zustand aller Partikel."""
    # 1. Berechne die Gravitationskräfte für alle Partikel
    for particle in particles:
        particle.force()

    # 2. Behandle Kollisionen zwischen Partikeln (jedes Paar wird nur einmal geprüft)
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            if (p1.r + p2.r) > p1.p.distance_to(p2.p):
                p1.collide(p2)

    # 3. Aktualisiere Geschwindigkeiten, Positionen und zeichne die Partikel
    for particle in particles:
        particle.velocity()
        particle.position()
        particle.draw()


def random_():
    """Gibt eine zufällige Position im Fenster zurück."""
    return random.randrange(0, width), random.randrange(0, height)


def is_near(spacing, x, y):
    """Überprüft, ob an (x, y) ein Partikel näher als 'spacing' ist."""
    test_vector = pygame.math.Vector2(x, y)
    for particle in particles:
        if particle.p.distance_to(test_vector) < spacing:
            return True
    return False


def new_random_location(spacing):
    """Ermittelt eine neue zufällige Position, die den Mindestabstand 'spacing' einhält."""
    x, y = random_()
    if not is_near(spacing, x, y):
        return x, y
    else:
        return new_random_location(spacing)


# Globale Parameter für die Einrichtung
global_amount = 0
global_spacing = 0
global_mass = 0


def setup(amount, spacing, mass):
    """Erzeugt 'amount' Partikel mit Mindestabstand 'spacing' und der Masse 'mass'."""
    global global_amount, global_spacing, global_mass
    global_amount = amount
    global_spacing = spacing
    global_mass = mass
    for _ in range(amount):
        x, y = new_random_location(spacing)
        Particle(x, y, mass)


def reset():
    """Setzt die Simulation zurück, indem alle Partikel gelöscht und neu erzeugt werden."""
    global particles
    particles.clear()
    setup(global_amount, global_spacing, global_mass)


# Initialisiere die Simulation (z. B. 10 Partikel, Mindestabstand 100, Masse 1e16)
setup(10, 100, 1e16)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Mit SPACE wird die Simulation zurückgesetzt
            if event.key == pygame.K_SPACE:
                reset()

    screen.fill("white")
    update()
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
