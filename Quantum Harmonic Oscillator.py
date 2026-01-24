import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import animation
from math import factorial
from scipy.special import hermite


n = 3
m = 9.11e-31
w = 2 * np.pi
hbar = 1.054571817e-34

scale = 1e-1
yscale = 200

fig = plt.figure(figsize=(14,10))
ax1 = plt.subplot(1,2,1)
ax1.set_xlim(-scale, scale)
ax1.set_ylim(-yscale,yscale)
plt.xlabel("x")
plt.ylabel(r"$|\psi_" + str(n) + "(x)|^2$")

# Subplot für Phase-Vektor im Einheitskreis
ax2 = plt.subplot(1,2,2)
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.set_xlabel("Re")
ax2.set_ylabel("Im")
ax2.set_title("Phase Factor")

# Zeichne den Einheitskreis mit Farbverlauf
theta = np.linspace(0, 2*np.pi, 256)
for i in range(len(theta)-1):
    color = plt.cm.hsv(theta[i]/(2*np.pi))
    ax2.plot(np.cos(theta[i:i+2]), np.sin(theta[i:i+2]), color=color, linewidth=2)

# Initialisiere den Vektor-Plot
quiver = ax2.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=1, width=0.006)



def xi(x):
    return np.sqrt(m * w / hbar) * x


def oscillator(x):
    Hn = hermite(n)          
    prefactor = (m*w/(np.pi*hbar))**0.25
    norm = 1 / np.sqrt(2**n * factorial(n))
    return prefactor * norm * Hn(xi(x)) * np.exp(-0.5 * xi(x)**2)

def time_evolution(t):
    energy_n = hbar * w * (n + 0.5)
    phase_factor = np.exp(-1j * energy_n * t / hbar)
    return phase_factor

# Animation
def animate(frame):
    t = frame * 0.001
    phase = time_evolution(t)
    
    phase_angle = np.angle(phase)
    phase_norm = (phase_angle % (2*np.pi)) / (2*np.pi)
    color = plt.cm.hsv(phase_norm)

    # Farbe der Wahrscheinlichkeitsdichte
    line.set_color(color)

    # Phasenvektor
    quiver.set_UVC(np.real(phase), np.imag(phase))
    quiver.set_color(color)

    return line, quiver

    

x_data = np.linspace(-scale, scale, 10_000)
y_data = np.abs(oscillator(x_data))**2


line, = ax1.plot(x_data, y_data)

ani = animation.FuncAnimation(fig, animate, frames=1000, interval=100)

plt.show()
