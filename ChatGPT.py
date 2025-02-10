import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameter der Feder-Dämpfer-System
m = 20  # Masse
k = 70  # Federkonstante
r = 10  # Radius des Kreises

dt = 0.01  # Zeitinkrement
s = float(input("Displacement: "))  # Anfangsauslenkung
v = 0  # Anfangsgeschwindigkeit

time_data = []
displacement_data = []
t = 0


def force(s):
    return -k * s


def update(frame):
    global s, v, t

    F = force(s)
    v += (F / m) * dt
    s += v * dt
    t += dt

    time_data.append(t)
    displacement_data.append(s)
    ax2.clear()
    ax2.plot(time_data, displacement_data, color='blue')
    ax2.set_title("Displacement vs Time")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Displacement")

    # Update der Position des Kreises
    circle.set_center((0, -s * 5))
    line.set_ydata([-s * 5, 0])

    return circle, line


# Erstellen der Matplotlib-Figur
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
ax1.set_xlim(-50, 50)
ax1.set_ylim(-100, 20)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_frame_on(False)

# Zeichnen der Feder und Masse
line, = ax1.plot([0, 0], [-s * 5, 0], color='mediumseagreen', linewidth=5)
circle = plt.Circle((0, -s * 5), r, color='black', fill=False)
ax1.add_patch(circle)

ax2.set_xlim(0, 10)
ax2.set_ylim(-s * 1.5, s * 1.5)
ax2.set_title("Displacement vs Time")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Displacement")

# Animation erstellen
ani = animation.FuncAnimation(fig, update, frames=1000, interval=dt * 1000, blit=False)
plt.show()