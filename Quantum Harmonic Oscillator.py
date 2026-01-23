import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from scipy.special import hermite

# Parameter
n = 15
m = 9.11e-31
w = 2 * np.pi
hbar = 1.054571817e-34

scale = 1e-1
yscale = 200

# dimensionslose Variable
def xi(x):
    return np.sqrt(m * w / hbar) * x

# Eigenfunktion
def oscillator(x):
    Hn = hermite(n)          # physikalisches Hermite-Polynom
    prefactor = (m*w/(np.pi*hbar))**0.25
    norm = 1 / np.sqrt(2**n * factorial(n))
    return prefactor * norm * Hn(xi(x)) * np.exp(-0.5 * xi(x)**2)

# Plot
x_data = np.linspace(-scale, scale, 10_000)
y_data = np.abs(oscillator(x_data))**2

plt.figure(figsize=(10,10))
plt.plot(x_data, y_data)
plt.xlim(-scale, scale)
plt.ylim(0, yscale)
plt.xlabel("x")
plt.ylabel(r"$|\psi_" + str(n) + "(x)|^2$")
plt.show()
