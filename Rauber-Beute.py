import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Erstelle eine 3D-Achse
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# --- 1. S-Orbitale als Wireframe-Sphären ---
# Erzeuge Gitter für eine Kugel
phi, theta = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]

# 1s-Orbital (kleiner Radius)
r1 = 0.8
x1 = r1 * np.sin(theta) * np.cos(phi)
y1 = r1 * np.sin(theta) * np.sin(phi)
z1 = r1 * np.cos(theta)
ax.plot_wireframe(x1, y1, z1, color='gray', linestyle='--', alpha=0.6, label='1s-Orbital')

# 2s-Orbital (größerer Radius)
r2 = 1.4
x2 = r2 * np.sin(theta) * np.cos(phi)
y2 = r2 * np.sin(theta) * np.sin(phi)
z2 = r2 * np.cos(theta)
ax.plot_wireframe(x2, y2, z2, color='gray', linestyle='--', alpha=0.6, label='2s-Orbital')

# --- 2. P-Orbitale als schematische Ellipsoide ---
# Erzeuge Gitter für Ellipsoide
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 25)
U, V = np.meshgrid(u, v)

# Parameter für die Ellipsoide (schematische Darstellung)
a = 0.3  # "Breite" des Lappens
b = 1.0  # "Länge" des Lappens

# p_x-Orbital: Lappen entlang der X-Achse
# Positiver Lappen
x_px_pos = 0.8 + b * np.cos(U) * np.sin(V)
y_px_pos = a * np.sin(U) * np.sin(V)
z_px_pos = a * np.cos(V)
ax.plot_surface(x_px_pos, y_px_pos, z_px_pos, color='r', alpha=0.6)
# Negativer Lappen
x_px_neg = -0.8 + b * np.cos(U) * np.sin(V)
y_px_neg = a * np.sin(U) * np.sin(V)
z_px_neg = a * np.cos(V)
ax.plot_surface(x_px_neg, y_px_neg, z_px_neg, color='r', alpha=0.6)

# p_y-Orbital: Lappen entlang der Y-Achse
# Positiver Lappen
x_py_pos = a * np.sin(U) * np.sin(V)
y_py_pos = 0.8 + b * np.cos(U) * np.sin(V)
z_py_pos = a * np.cos(V)
ax.plot_surface(x_py_pos, y_py_pos, z_py_pos, color='g', alpha=0.6)
# Negativer Lappen
x_py_neg = a * np.sin(U) * np.sin(V)
y_py_neg = -0.8 + b * np.cos(U) * np.sin(V)
z_py_neg = a * np.cos(V)
ax.plot_surface(x_py_neg, y_py_neg, z_py_neg, color='g', alpha=0.6)

# p_z-Orbital: Lappen entlang der Z-Achse
# Positiver Lappen
x_pz_pos = a * np.sin(U) * np.sin(V)
y_pz_pos = a * np.cos(U) * np.sin(V)
z_pz_pos = 0.8 + b * np.cos(V)
ax.plot_surface(x_pz_pos, y_pz_pos, z_pz_pos, color='b', alpha=0.6)
# Negativer Lappen
x_pz_neg = a * np.sin(U) * np.sin(V)
y_pz_neg = a * np.cos(U) * np.sin(V)
z_pz_neg = -0.8 + b * np.cos(V)
ax.plot_surface(x_pz_neg, y_pz_neg, z_pz_neg, color='b', alpha=0.6)

# --- 3. Kern einzeichnen ---
ax.scatter(0, 0, 0, color='k', s=100, label='Kern')

# --- Achsenformatierung ---
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("Schematische 3D-Darstellung der Stickstoff-Orbitale")
ax.legend(loc='upper left')

plt.show()
