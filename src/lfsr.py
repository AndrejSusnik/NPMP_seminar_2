from models import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
    

"""
    TESTING
"""

# simulation parameters
t_end = 300 * 2
N = 10000 * 2


# model parameters
alpha1 = 34.73 # protein_production
alpha2 = 49.36 # protein_production
alpha3 = 32.73 # protein_production
alpha4 = 49.54 # protein_production
delta1 = 1.93 # protein_degradation
delta2 = 0.69 # protein_degradation
Kd = 10.44 # Kd
n = 4.35 # hill

params_ff = (alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n)

Y0 = np.array([100] + [0] * 42)
T = np.linspace(0, t_end, N) # vector of timesteps

# numerical interation
# Y = odeint(four_bit_lfsr_34, Y0, T, args=(params_ff,))
Y = odeint(eight_bit_lfsr, Y0, T, args=(params_ff,))

Y_reshaped = np.split(Y, Y.shape[1], 1)
Q1 = Y_reshaped[2]
not_Q1 = Y_reshaped[3]
Q2 = Y_reshaped[6]
not_Q2 = Y_reshaped[7]
Q3 = Y_reshaped[10]
not_Q3 = Y_reshaped[11]
Q4 = Y_reshaped[14]
not_Q4 = Y_reshaped[15]

Q5 = Y_reshaped[18]
not_Q5 = Y_reshaped[19]
Q6 = Y_reshaped[22]
not_Q6 = Y_reshaped[23]
Q7 = Y_reshaped[26]
not_Q7 = Y_reshaped[27]
Q8 = Y_reshaped[30]
not_Q8 = Y_reshaped[31]



# Plot offset
# off = int(186 * N / t_end)
# T = T[off:]
# Q1 = Q1[off:]
# Q2 = Q2[off:]
# Q3 = Q3[off:]
# Q4 = Q4[off:]

plt.rcParams['figure.figsize'] = 8, 5

#plt.style.use('dark_background')

# plt.subplot(4, 1, 1)
plt.subplot(8, 1, 1)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q1, label='q1', color='tab:blue')
plt.legend()
plt.subplot(8, 1, 2)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q2, label='q2', color='tab:orange')
plt.legend()
plt.subplot(8, 1, 3)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q3, label='q3', color='tab:green')
plt.legend()
plt.subplot(8, 1, 4)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q4, label='q4', color='tab:red')
plt.legend()
plt.subplot(8, 1, 5)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q5, label='q5', color='tab:purple')
plt.legend()
plt.subplot(8, 1, 6)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q6, label='q6', color='tab:brown')
plt.legend()
plt.subplot(8, 1, 7)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q7, label='q7', color='tab:pink')
plt.legend()
plt.subplot(8, 1, 8)
plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
plt.plot(T, Q8, label='q8', color='tab:gray')
plt.legend()


plt.subplots_adjust(0.06, 0.05, 0.94, 0.95, hspace=0.28)
plt.show()