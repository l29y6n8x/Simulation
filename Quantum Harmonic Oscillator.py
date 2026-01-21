import matplotlib.pyplot as plt
import numpy as np
import math 



n = 2
m = 9.11 * 10**(-31)
w = 2*np.pi
h_bar = 1.054571817e-34
psi = 0

scale = 10e-3
yscale = 200

fig = plt.figure(figsize=(10,10))
ax = plt.subplot(1,1,1)
ax.set_xlim(-scale, scale)
ax.set_ylim(-yscale,yscale)

def fakultät(b):
    result = 1
    for i in range(b):
        result *= (i+1)
    return result

def H_func(c,d):
    if c == 0:
        return 1
    if c == 1:
        return 2 * d/(np.sqrt(h_bar/(m*w)))
    if c == 2:
        return (2 * d/(np.sqrt(h_bar/(m*w))))**2 - 2

def oscillator(a):
    psi = (m * w / (h_bar * np.pi))**(1/4) * 1/np.sqrt(math.factorial(n) * 2**n) * H_func(n,a) * np.e ** (-1/2 * (m * w / h_bar) * a ** 2)
    return psi



        



def display():
    ax.plot(x_data, y_data)
x_data = np.linspace(-scale,scale,10000)
y_data = (np.absolute(oscillator(x_data))**2)

display()

plt.show()