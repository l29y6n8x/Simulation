import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from math import factorial
from scipy.special import hermite
import matplotlib.colors as colors

# -------------------------------
# Physikalische Parameter
# -------------------------------
n = 3
m = 9.11e-31
w = 2 * np.pi
hbar = 1.054571817e-34

# -------------------------------
# Raumgitter
# -------------------------------
scale = 0.03
x_data = np.linspace(-scale, scale, 8000)

# -------------------------------
# Abbildungen
# -------------------------------
fig = plt.figure(figsize=(15, 10))

# |ψ|² mit Phase
ax1 = plt.subplot(2, 2, 2)
ax1.set_xlim(-scale, scale)
ax1.set_ylim(0, 250)
ax1.set_xlabel("x")
ax1.set_ylabel(r"$|\psi(x,t)|^2$")
ax1.set_title("Wellenfunktion + Phase")

# Eigenfunktionen
ax2 = plt.subplot(2, 2, 1)
ax2.set_xlim(-scale, scale)
ax2.set_title("Eigenfunktionen (Re / Im)")

# Phasenraum
ax3 = plt.subplot(2, 2, 3)
ax3.set_xlabel(r"$\langle x \rangle$")
ax3.set_ylabel(r"$\langle p \rangle$")
ax3.set_title("Phasenraum")
ax3.grid(True)

# -------------------------------
# Farbskala für Phase
# -------------------------------
norm_phase = colors.Normalize(vmin=-np.pi, vmax=np.pi)
scat = ax1.scatter(
    x_data,
    np.zeros_like(x_data),
    c=np.zeros_like(x_data),
    cmap="hsv",
    norm=norm_phase,
    s=2
)

cbar = plt.colorbar(scat, ax=ax1)
cbar.set_label("Phase arg(ψ)")
cbar.set_ticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
cbar.set_ticklabels(['-π', '-π/2', '0', 'π/2', 'π'])

# Norm-Anzeige
norm_text = ax1.text(
    0.02, 0.95, "",
    transform=ax1.transAxes,
    fontsize=11,
    verticalalignment="top"
)

# -------------------------------
# Hilfsfunktionen
# -------------------------------
def xi(x):
    return np.sqrt(m * w / hbar) * x

def oscillator(x, i):
    Hn = hermite(i)
    pref = (m * w / (np.pi * hbar))**0.25
    norm = 1 / np.sqrt(2**i * factorial(i))
    return pref * norm * Hn(xi(x)) * np.exp(-0.5 * xi(x)**2)

def time_evolution(t, i):
    E = hbar * w * (i + 0.5)
    return np.exp(-1j * E * t / hbar)

# -------------------------------
# Eigenfunktionen vorbereiten
# -------------------------------
y_data = [oscillator(x_data, i) for i in range(n + 1)]

real_lines = []
imag_lines = []

for i in range(n + 1):
    real_line, = ax2.plot(x_data, y_data[i] + i * 20, color="green")
    imag_line, = ax2.plot(x_data, y_data[i] + i * 20, color="red", linestyle="--")
    ax2.text(-scale * 0.95, i * 20 + 1, rf"$n={i}$")
    real_lines.append(real_line)
    imag_lines.append(imag_line)

# -------------------------------
# Phasenraum-Daten
# -------------------------------
x_vals = []
p_vals = []
phase_line, = ax3.plot([], [], color="black")
phase_point = ax3.scatter([], [], s=30)

# -------------------------------
# Animation
# -------------------------------
def animate(frame):
    t = frame * 0.01

    psi = np.zeros_like(x_data, dtype=complex)
    for i in range(n + 1):
        psi += (1 / np.sqrt(n + 1)) * y_data[i] * time_evolution(t, i)

    # Norm
    norm_val = np.trapezoid(np.abs(psi)**2, x_data)
    psi /= np.sqrt(norm_val)

    density = np.abs(psi)**2
    phase = np.angle(psi)
    phase[density < 1e-6] = np.nan

    scat.set_offsets(np.c_[x_data, density])
    scat.set_array(phase)
    norm_text.set_text(f"Norm = {norm_val:.5f}")

    # Eigenfunktionen
    for i in range(n + 1):
        pf = time_evolution(t, i)
        real_lines[i].set_ydata(np.real(y_data[i] * pf) + i * 20)
        imag_lines[i].set_ydata(np.imag(y_data[i] * pf) + i * 20)

    # Erwartungswerte
    x_exp = np.trapezoid(x_data * density, x_data)
    dpsi_dx = np.gradient(psi, x_data)
    p_exp = np.trapezoid(np.conj(psi) * (-1j * hbar * dpsi_dx), x_data).real

    x_vals.append(x_exp)
    p_vals.append(p_exp)

    phase_line.set_data(x_vals, p_vals)
    phase_point.set_offsets([[x_exp, p_exp]])

    return scat, phase_line, phase_point

ani = animation.FuncAnimation(
    fig,
    animate,
    frames=800,
    interval=40,
    blit=False
)

plt.tight_layout()
plt.show()
