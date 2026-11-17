import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy import integrate

hbar = 1.054571817e-34


scale = 100

x_data = np.linspace(-scale, scale, 1000)

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(1, 1, 1)
ax.set_xlim(-scale, scale)

def eigenfunction(x,p):
    integrant = np.exp(-1j * p * x / hbar)
    return integrant
    
def wavefunction(x, pmax=1e-34):
    # Analytische Integralformel: int_0^pmax exp(-i*p*x/hbar) dp
    # = (-i*hbar/x) * (exp(-i*pmax*x/hbar) - 1)  fuer x != 0
    # = pmax  fuer x = 0
    x_arr = np.asarray(x)
    
    def psi_scalar(xi):
        if np.abs(xi) < 1e-15:
            return pmax
        return (-1j * hbar / xi) * (np.exp(-1j * pmax * xi / hbar) - 1)
    
    if x_arr.ndim == 0:
        return psi_scalar(x_arr.item())
    return np.vectorize(psi_scalar)(x_arr)

#y_data = np.abs(wavefunction(x_data))**2
y_data= wavefunction(x_data)
ax.plot(x_data, y_data)
plt.xlabel("x")
plt.ylabel(r"$|\psi(x)|^2$")
plt.title("Free Particle Wavefunction Probability Density")
plt.show()