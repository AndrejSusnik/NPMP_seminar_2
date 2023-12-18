from models import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
    

"""
    TESTING
"""

# simulation parameters
t_end = 200
N = 1000


# model parameters
alpha1 = 34.73 # protein_production
alpha2 = 49.36 # protein_production
alpha3 = 32.73 # protein_production
alpha4 = 49.54 # protein_production
delta1 = 1.93 # protein_degradation
delta2 = 0.69 # protein_degradation
Kd = 10.44 # Kd
n = 4.35 # hill

params_ff = (alpha1, delta1, Kd, n)


# three-bit counter with external clock
# a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3
Y0 = np.array([120] + [0]*4) # initial state
T = np.linspace(0, t_end, N) # vector of timesteps

# numerical interation
Y = odeint(xor_model, Y0, T, args=(params_ff,))

Y_reshaped = np.split(Y, Y.shape[1], 1)

# plotting the results
X1 = Y_reshaped[0]
X2 = Y_reshaped[2]
Y = Y_reshaped[4]

plt.plot(T, X1, label='x1')
plt.plot(T, X2, label='x2')
plt.plot(T, Y, label='y')
#plt.plot(T, not_Q1, label='not q1')
#plt.plot(T, not_Q2, label='not q2')

plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)

plt.legend()
plt.show()
