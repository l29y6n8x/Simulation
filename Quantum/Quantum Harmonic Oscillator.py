import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import animation
from math import factorial
from scipy.special import hermite
import matplotlib.colors as colors

n = 7 
m = 9.11e-31
w = 2 * np.pi
hbar = 1.054571817e-34

x_data = []
y_data = []
phase = []
y = 0

scale = 0.3 * 1e-1
yscale = 250

fig = plt.figure(figsize=(14,10))
ax1 = plt.subplot(1,2,2)
ax1.set_xlim(-scale, scale)
ax1.set_ylim(0,yscale)
ax1.title.set_text("Harmonic Oscillator")
plt.xlabel("x")
plt.ylabel(r"$|\psi(x, t)|^2$")


ax2 = plt.subplot(1,2,1)
ax2.set_xlim(-scale, scale)
ax2.title.set_text("Eigenfunctions")


norm = colors.Normalize(vmin=-np.pi, vmax=np.pi)

scat = ax1.scatter(
    x_data,
    np.zeros_like(x_data),
    c=np.zeros_like(x_data),
    cmap='hsv',
    norm=norm,
    s=2
)

cbar = plt.colorbar(scat, ax=ax1)
cbar.set_ticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
cbar.set_ticklabels(['-π', '-π/2', '0', 'π/2', 'π'])
cbar.set_label("Phase arg(ψ)")


def xi(x):
    return np.sqrt(m * w / hbar) * x


def oscillator(x,i):
    Hn = hermite(i)          
    prefactor = (m*w/(np.pi*hbar))**0.25
    norm = 1 / np.sqrt(2**i * factorial(i))
    return prefactor * norm * Hn(xi(x)) * np.exp(-0.5 * xi(x)**2)

def time_evolution(t,i):
    energy_n = hbar * w * (i + 0.5)
    phase_factor = np.exp(-1j * energy_n * t / hbar)
    return phase_factor

def eigenstates():
    for i in range(n+1):
        ax2.plot(x_data, y_data[i] + i*20, color ='green')
        ax2.text(-scale+scale*0.01, i*20+1, r"$E_{" + str(i) + "}$")

    for i in range(n+1):
        ax2.plot(x_data, y_data[i] + i*20, color='red', linestyle="--")

# Animation
def animate(frame):
    t = frame * 0.01

    phase_factors = [time_evolution(t, i) for i in range(n+1)]

    psi = np.zeros_like(x_data, dtype=complex)
    for i in range(n+1):
        psi += (1/np.sqrt(n+1)) * y_data[i] * phase_factors[i]

    phase = np.angle(psi)
    density = np.abs(psi)**2

    scat.set_offsets(np.c_[x_data, density])
    scat.set_array(phase)

#eigenfunctions
    for i in range(n+1):
        ax2.lines[i].set_ydata(np.real((y_data[i] * phase_factors[i]) + i*20))

    for j in range(n+1):
        ax2.lines[j + n + 1].set_ydata(np.imag((y_data[j] * phase_factors[j]))+ j*20)

    return scat

x_data = np.linspace(-scale, scale, 10_000)  
for i in range(n+1):
    y_data.append(oscillator(x_data,i))

eigenstates()

ani = animation.FuncAnimation(fig, animate, frames=1000, interval=100)
# Uncomment the following lines to save the animation as an MP4 file
#try:
#    Writer = animation.FFMpegWriter
#    writer = Writer(fps=30, metadata=dict(artist='User'), bitrate=1800)
#    ani.save('harmonic_oscillator.mp4', writer=writer, dpi=200)
#    print("Animation saved to harmonic_oscillator.mp4")
#except Exception as e:
#    print("Fehler beim Speichern als MP4. Stelle sicher, dass ffmpeg installiert ist und im PATH liegt.")
#    print(e)#

plt.show()