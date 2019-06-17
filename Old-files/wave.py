import multiprocessing

import numpy as np
import matplotlib.pyplot as plt
import scipy as s
import scipy.io as io
import random

import seaborn as sns
import math

print('wlerjk')

init_conc_rd = 1000

concentration = init_conc_rd
kinetic_constant = 0.5

max_t = 100000000
max_steps = 10000000

t = 0
step = 0

def hfactor(x):
    return x

def propensity(x, ke):
    return ke*hfactor(x)

plot_y = [] #concentration
plot_x = [] #time
plot_y.append(concentration)
plot_x.append(t)


while t < max_t and step < max_steps:
    
    if concentration <= 1:
        break
    
    a0 = propensity(concentration, kinetic_constant)
    r1, r2 = np.random.random(2) 
    
    T = (1/a0)*np.log(1/r1)

    concentration -= 1
        
    t+= T; step += 1;
    plot_y.append(concentration)
    plot_x.append(t)

plt. plot(plot_x, plot_y)
plt.show()

theor_x = plot_x
theor_y = [ init_conc_rd * np.exp(-kinetic_constant*t) for t in plot_x]

plt.plot(theor_x, theor_y)
plt.show()

plt.plot(theor_x, theor_y,plot_x, plot_y)
plt.show()