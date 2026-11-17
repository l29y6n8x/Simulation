import pygame
import numpy as np
from arrow import draw_arrow
from Projection import Cameraframe
from Inputs import Camera

class Particles:
    def __init__(self):
        position = np.array([0.0 , 0.0, 40.0])
        velocity = np.array([0.0, 0.0, 0.0])
        acceleration = np.array([0.0, 0.0, 0.0])
        self.state = np.array([position, velocity, acceleration])
        
        self.charge = 1.0
        self.mass = 1.0
        self.radius = 10

class Integration:
    def __init__(self):
        self.dt = 0.1
        self.k = 1  # Coulomb's constant


    def DEQ(self, state, particle):
        particle.state[2] = -self.k * state[0] / particle.mass
        x_dot = state[1]
        x_ddot = particle.state[2]
        return np.array([x_dot, x_ddot])

    

    def update(self, particle):
        #print(particle.state[0:2])
        k1 = self.DEQ(particle.state[0:2], particle)
        k2 = self.DEQ(particle.state[0:2] + 0.5 * self.dt * k1, particle)
        k3 = self.DEQ(particle.state[0:2] + 0.5 * self.dt * k2, particle)
        k4 = self.DEQ(particle.state[0:2] + self.dt * k3, particle)
        particle.state[0:2] += (self.dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        particle.state[2] = -self.k * particle.state[0] / particle.mass
        return particle.state


class vector_calculus:
    def _value(self, vector_field, index, component):
        if index < 0 or index >= len(vector_field):
            return None
        vector = vector_field[index][1]
        if vector[0] is None:
            return None
        return vector[component]

    def _partial(self, vector_field, i, stride, axis_index, axis_size, step, component):
        center = self._value(vector_field, i, component)
        if center is None:
            return None

        forward = self._value(vector_field, i + stride, component) if axis_index < axis_size - 1 else None
        backward = self._value(vector_field, i - stride, component) if axis_index > 0 else None

        if forward is not None and backward is not None:
            return (forward - backward) / (2 * step)
        if forward is not None:
            return (forward - center) / step
        if backward is not None:
            return (center - backward) / step
        return None

    def curl(self, vector_field, step_size, size):
        ix, iy, iz = 3 * size, 3, 1
        z_size = 3

        curl_V_field = []
        for i in range(len(vector_field)):
            if vector_field[i][1][0] is None:
                curl_V_field.append(None)
                continue

            x = i // ix
            y = (i // iy) % size
            z = i % z_size

            dVy_dx = self._partial(vector_field, i, ix, x, size, step_size, component=1)
            dVz_dx = self._partial(vector_field, i, ix, x, size, step_size, component=2)
            dVx_dy = self._partial(vector_field, i, iy, y, size, step_size, component=0)
            dVz_dy = self._partial(vector_field, i, iy, y, size, step_size, component=2)
            dVx_dz = self._partial(vector_field, i, iz, z, z_size, step_size, component=0)
            dVy_dz = self._partial(vector_field, i, iz, z, z_size, step_size, component=1)

            if None in (dVy_dx, dVz_dx, dVx_dy, dVz_dy, dVx_dz, dVy_dz):
                curl_V_field.append(None)
                continue

            curl_x = dVz_dy - dVy_dz
            curl_y = dVx_dz - dVz_dx
            curl_z = dVy_dx - dVx_dy

            curl_V = np.array([curl_x, curl_y, curl_z])
            curl_V_field.append(curl_V)

        return curl_V_field

     

class Potential_Method:    
    def __init__(self):
        self.k = 8.9875517873681764e9  # Coulomb's constant
        self.c = 100  # Speed of light
        self.step_size = 50
        self.size = 15
        self.calc = vector_calculus()

        x, y, z = np.meshgrid(
            np.arange(self.size),
            np.arange(self.size),
            np.arange(3),
            indexing="ij"
        )
        

        self.points = np.stack([
            (x - self.size // 2) * self.step_size,
            (y - self.size // 2) * self.step_size,
            (z - 1) * self.step_size
        ], axis=-1).reshape(-1, 3).astype(float)

        self.B_vector_field = [
                    (point, np.zeros(3))
                    for point in self.points
                ]

    def electric_field(self, history):
        self.dt = 0.1
        particle = Particles()
        self.E_vector_field = []
        self.B_vector_field = []
        self.max_E_magnitude = 0.0

        for point in self.points:
            difference = point - history[0][0]
            distance = np.linalg.norm(difference)
            index = np.rint(distance / (self.c * self.dt)).astype(int)

            if distance < (particle.radius + 10):
                invalid_vector = np.array([None, None, None], dtype=object)
                self.E_vector_field.append((point, invalid_vector))
                self.B_vector_field.append((point, invalid_vector.copy()))
                continue

            gamma = 1 / np.sqrt(1 - (np.linalg.norm(history[index][1]) / self.c) ** 2) if np.linalg.norm(history[index][1]) > 0 else 1.0
            d_vector = difference - history[index][1] * (distance / self.c)
            d_scalar = distance - np.dot(difference, history[index][1]) / self.c
            q = particle.charge

            coulomb_part = self.k * (q * d_vector) / (gamma ** 2 * d_scalar ** 3)
            radiation_part = self.k * (q * np.cross(d_vector, np.cross(d_vector, history[index][2]))) / (self.c ** 2 * d_scalar ** 3)
            E = coulomb_part + radiation_part
            B = 1 / self.c * np.cross(difference / distance, E)

            self.E_vector_field.append((point, E))
            self.B_vector_field.append((point, B))

        scaling = 1.0
        self.max_E_magnitude = 1/scaling * self.k * particle.charge / particle.radius**2 * (1-0.9)/(1-0.9)**1.5 + self.k * (particle.charge * np.linalg.norm(history[0][2])) / (self.c ** 2 * particle.radius)
        self.max_B_magnitude =1/scaling * self.max_E_magnitude / self.c
        #valid_e_fields = (
        #    E for _, E in self.E_vector_field
        #    if E is not None and not any(component is None for component in E)
        #)
        #valid_b_fields = (
        #    B for _, B in self.B_vector_field
        #    if B is not None and not any(component is None for component in B)
        #)
        #self.max_E_magnitude = max(
        #    (np.linalg.norm(E) for E in valid_e_fields),
        #    default=0.0,
        #)
        #self.max_B_magnitude = max(
        #    (np.linalg.norm(B) for B in valid_b_fields),
        #    default=0.0,
        #)
        return self.E_vector_field, self.B_vector_field

    def current_density(self, history, charge):
        J = np.zeros((self.size, self.size, 3, 3))

        position = history[0][0]# + np.array([0, 100, 0])  # Position of the particle
        velocity = history[0][1]

        # Position of the grid origin
        origin = np.array([
            -self.size // 2 * self.step_size,
            -self.size // 2 * self.step_size,
            -self.step_size
        ])

        # Position in grid coordinates
        grid_position = (position - origin) / self.step_size 

        # Lower grid indices
        base = np.floor(grid_position).astype(int)

        # Fractional position within the cell
        fraction = grid_position - base

        # Distribute current to the 8 surrounding grid points
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):

                    index = base + np.array([dx, dy, dz])

                    if not (
                        0 <= index[0] < self.size
                        and 0 <= index[1] < self.size
                        and 0 <= index[2] < 3
                    ):
                        continue

                    wx = fraction[0] if dx else 1 - fraction[0]
                    wy = fraction[1] if dy else 1 - fraction[1]
                    wz = fraction[2] if dz else 1 - fraction[2]

                    weight = wx * wy * wz 

                    cell_volume = (self.step_size*1) ** 3

                    J[tuple(index)] += (
                        charge * velocity * weight / cell_volume
                    )

        # Convert the 3D grid into the same flattened format as self.points
        return [
            (self.points[i], J.reshape(-1, 3)[i])
            for i in range(len(self.points))
        ]
    
    def maxwell(self, history, charge):

        # Calculate curls
        curl_E = self.calc.curl(
            self.E_vector_field,
            self.step_size,
            self.size
        )

        curl_B = self.calc.curl(
            self.B_vector_field,
            self.step_size,
            self.size
        )
        #print(curl_B)

        # Calculate current density
        J_vector_field = self.current_density(history, charge)

        # Vacuum permittivity, derived from Coulomb's constant
        epsilon_0 = 1 / (4 * np.pi * self.k)

        dB_dt = []
        dE_dt = []

        for i in range(len(self.points)):

            if curl_E[i] is None:
                dB_dt.append(np.zeros(3))
            else:
                dB_dt.append(-curl_E[i])

            if curl_B[i] is None:
                curl = np.zeros(3)
            else:
                
                curl = curl_B[i]

            J = J_vector_field[i][1]

            #curl = 0
            

            dE = self.c**2 * curl - J / epsilon_0
            #print(dB_dt[i])
            print(J)

            dE_dt.append(dE)
        #print("dE_dt:", dE_dt)
        return dB_dt, dE_dt

    def electromagnetic_field(self, history):
        dt = 0.01
        particle = Particles()
        self.E_vector_field = []
        
        self.max_E_magnitude = 0.0

        for i, point in enumerate(self.points):
            difference = point - history[0][0]
            distance = np.linalg.norm(difference)
            normal_d = difference / distance if distance != 0 else np.array([0.0, 0.0, 0.0])
            index = np.rint(distance / (self.c * dt)).astype(int)

            if distance < (particle.radius ):
                invalid_vector = np.array([None, None, None], dtype=object)
                self.E_vector_field.append((point, invalid_vector))
                self.B_vector_field[i] = (point, invalid_vector.copy())
                continue


            beta = np.linalg.norm(history[index][1]) / self.c
            gamma = 1 / np.sqrt(1 - beta ** 2) if beta < 1 else 1.0
            normal_v = history[index][1] / np.linalg.norm(history[index][1]) if np.linalg.norm(history[index][1]) != 0 else np.array([0.0, 0.0, 0.0])
            E = self.k * (particle.charge * difference) / (distance ** 3) * (1 - beta ** 2) / (1 - beta ** 2 * (1 - np.dot(normal_d, normal_v)) ** 2) ** (3 / 2)
            self.E_vector_field.append((point, E))

        dB_dt, dE_dt = self.maxwell(history, particle.charge)
        if self.B_vector_field is None:
            self.B_vector_field = [(point, np.array([0.0, 0.0, 0.0], dtype=object)) for point in self.points]
        for i in range(len(self.points)):
            if any(component is None for component in self.E_vector_field[i][1]):
                continue
            if any(component is None for component in self.B_vector_field[i][1]):
                continue
            self.B_vector_field[i] = (self.points[i], self.B_vector_field[i][1] + dB_dt[i] * dt)
            self.E_vector_field[i] = (self.points[i], self.E_vector_field[i][1] + dE_dt[i] * dt)
        scaling = 1.0
        self.max_E_magnitude = 1/scaling * self.k * particle.charge / particle.radius**2 * (1-0.9)/(1-0.9)**1.5 + self.k * (particle.charge * np.linalg.norm(history[0][2])) / (self.c ** 2 * particle.radius)
        self.max_B_magnitude =1/scaling * self.max_E_magnitude / self.c
        #valid_e_fields = (
        #    E for _, E in self.E_vector_field
        #    if E is not None and not any(component is None for component in E)
        #)
        #valid_b_fields = (
        #    B for _, B in self.B_vector_field
        #    if B is not None and not any(component is None for component in B)
        #)
        #self.max_E_magnitude = max(
        #    (np.linalg.norm(E) for E in valid_e_fields),
        #    default=0.0,
        #)
        #self.max_B_magnitude = max(
        #    (np.linalg.norm(B) for B in valid_b_fields),
        #    default=0.0,
        #)
                


class Animation:
    def __init__(self, particles):
        self.frame_rate = 100
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Maxwell')
        self.running = True
        self.clock = pygame.time.Clock()
        self.last_update_time = pygame.time.get_ticks()
        self.cameraframe = Cameraframe(300, [0, 0])
        self.camera = Camera(1/self.frame_rate)
        self.former = None
        self.EM = Potential_Method()
        self.storage_duration = int((np.sqrt(2 * self.EM.size ** 2 + 4) * self.EM.step_size // self.EM.c) * self.frame_rate)
        self.particles_history = []
        for _ in range(self.storage_duration):
            self.particles_history.append(particles.state)
        

    def store_values(self, particles, E_fields, B_fields):
        self.former_particles = particles.state.copy()
        self.particles_history = np.roll(self.particles_history, 1, axis=0)
        self.particles_history[0] = self.former_particles
        self.former_E_field = E_fields
        self.former_B_field = B_fields
        self.former = True

    def run_animation(self, particles):
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                camera_distance, orientation = self.camera.move_camera(event)
                self.cameraframe = Cameraframe(camera_distance, orientation)

            particles.state = Integration().update(particles)
            

            if self.former is None:
                self.EM.electric_field(self.particles_history)
                #self.EM.electromagnetic_field(self.particles_history)
                E_field = self.EM.E_vector_field
                B_field = self.EM.B_vector_field
                self.store_values(particles, E_field, B_field)

            if (
                np.linalg.norm(particles.state[0] - self.former_particles[0]) > 1e-5
                or np.linalg.norm(particles.state[1] - self.former_particles[1]) > 1e-2
            ):
                self.EM.electric_field(self.particles_history)
                #self.EM.electromagnetic_field(self.particles_history)
                E_field = self.EM.E_vector_field
                B_field = self.EM.B_vector_field
                self.store_values(particles, E_field, B_field)

            self.screen.fill((0, 0, 0))
            
            body2D, radius = self.cameraframe.project(particles)

            width, height = self.screen.get_size()

            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (body2D + np.array([width // 2, height // 2], dtype=float)).astype(int),
                radius,
            )

            max_E_magnitude = self.EM.max_E_magnitude
            if max_E_magnitude == 0:
                max_E_magnitude = 1.0
    
            self.draw_vector_field(self.EM.E_vector_field, max_E_magnitude, particles, color_index=0)

            max_B_magnitude = self.EM.max_B_magnitude
            if max_B_magnitude == 0:
                max_B_magnitude = 1.0

            self.draw_vector_field(self.EM.B_vector_field, max_B_magnitude, particles, color_index=1)

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def draw_vector_field(self, vector_field, max_magnitude, particles, color_index):
        width, height = self.screen.get_size()

        for point, vector in vector_field:
            if point[2]==0 and point[1]==0:

                if vector is None or any(component is None for component in vector):
                    continue
                if np.linalg.norm(vector) <= particles.radius or np.linalg.norm(point) <= particles.radius:
                    continue
                projected_point = self.cameraframe.project_point(point)
                if projected_point is None:
                    continue
                start = pygame.Vector2(*((projected_point + np.array([width // 2, height // 2], dtype=float)).tolist()))
                direction = np.sqrt((np.linalg.norm(vector) / max_magnitude))
                direction = np.sqrt(direction) * vector / np.linalg.norm(vector) * self.EM.step_size 
                #direction = direction / np.linalg.norm(direction) * self.EM.step_size
                if np.linalg.norm(direction) > 4:

                    projected_direction = self.cameraframe.project_point(direction*3)
                    if projected_direction is None:
                        continue
                    end = start + pygame.Vector2(projected_direction.tolist())
                    color_intensity = int(55 * (np.linalg.norm(direction) / self.EM.step_size))

                    #print(np.linalg.norm(projected_direction))
                    draw_arrow(
                        self.screen,
                        start,
                        end,
                        pygame.Color(0, 200 + color_intensity, 200 * color_index + color_index * color_intensity),
                        body_width=0.05 * np.linalg.norm(projected_direction),
                        head_width=0.25 * np.linalg.norm(projected_direction),
                        head_height=0.125 * np.linalg.norm(projected_direction),
                    )
    
        

if __name__ == "__main__":
    particles = Particles()
    run_animation = Animation(particles)
    run_animation.run_animation(particles)