import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def lotka_volterra(t, y, alpha, beta, delta, gamma):
    prey, predator = y
    dydt = [alpha * prey - beta * prey * predator,
            delta * prey * predator - gamma * predator]
    return np.array(dydt)


def rk4_step(f, t, y, dt, *args):
    k1 = f(t, y, *args)
    k2 = f(t + dt / 2, y + dt / 2 * k1, *args)
    k3 = f(t + dt / 2, y + dt / 2 * k2, *args)
    k4 = f(t + dt, y + dt * k3, *args)
    return y + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate(alpha, beta, delta, gamma, y0, t_span, dt):
    t_values = np.arange(t_span[0], t_span[1], dt)
    y_values = np.zeros((len(t_values), len(y0)))

    y = y0
    for i, t in enumerate(t_values):
        y_values[i] = y
        y = rk4_step(lotka_volterra, t, y, dt, alpha, beta, delta, gamma)

    return t_values, y_values


# Parameterwerte
alpha = 0.1  # Wachstumsrate der Beute
beta = 0.02  # Rate, mit der Raubtiere Beute fangen
delta = 0.01  # Rate, mit der Raubtiere durch Fressen der Beute wachsen
gamma = 0.1  # Sterberate der Raubtiere

# Anfangsbedingungen (Beute, Räuber)
y0 = [40, 9]

# Simulationsparameter
t_span = (0, 200)  # Simulationsdauer
dt = 0.1  # Zeitschritt

t_values, y_values = simulate(alpha, beta, delta, gamma, y0, t_span, dt)

# Erstellung der Animation
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(t_span[0], t_span[1])
ax.set_ylim(0, max(y_values[:, 0].max(), y_values[:, 1].max()) * 1.1)
ax.set_xlabel('Zeit')
ax.set_ylabel('Population')
ax.set_title('Räuber-Beute-Dynamik mit RK4')
sc_prey = ax.scatter([], [], color='blue', label='Beute', s=10)
sc_predator = ax.scatter([], [], color='red', label='Räuber', s=10)
ax.legend()


def update(frame):
    sc_prey.set_offsets(np.c_[t_values[:frame], y_values[:frame, 0]])
    sc_predator.set_offsets(np.c_[t_values[:frame], y_values[:frame, 1]])
    return sc_prey, sc_predator


ani = animation.FuncAnimation(fig, update, frames=len(t_values), interval=30, blit=True)
plt.show()
