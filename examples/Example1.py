# Example 1 will illustrate the calculations of light reflectances for one 
# stack of three layers on a semi-infinite substrate. Semi-infinite is the 
# term for a substrate where there is no beam coming back from the 
# rear of the substrate. 
 
 
# Example1.py 
 
# -*- coding: utf-8 -*- 
import os


import numpy as np
import matplotlib.pyplot as plt

from Funcs import calc_rsrpTsTp
 
# Define parameters
nlamb = 31
x = np.linspace(400, 700, nlamb)

# Define layers
layers = [
    [np.nan, "Constant", [1., 0.]],
    [93, "Cauchy", [1.36, 4100., 0., 0., 0.]],
    [121, "Cauchy", [2.0, 17500., 98000., 0., 0.]],
    [185, "Cauchy", [1.36, 4100., 0., 0., 0.]],
    [np.nan, "BK7", [0]]
]

# Define incidence angle
incang = np.zeros(x.size)

# Calculate reflectance for normal incidence
rs, rp, Ts, Tp = calc_rsrpTsTp(incang, layers, x)
R0 = np.abs(rs) ** 2

# Calculate reflectance for 40 degrees incidence angle
incang_40 = 40 * np.pi / 180 * np.ones(x.size)
rs_40, rp_40, Ts_40, Tp_40 = calc_rsrpTsTp(incang_40, layers, x)
Rs40 = np.abs(rs_40) ** 2
Rp40 = np.abs(rp_40) ** 2

# Define layers for no layers case
NO_layers = [
    [np.nan, "Constant", [1., 0.]],
    [np.nan, "BK7", [0]]
]

# Calculate reflectance for no layers
rs_no, rp_no, Ts_no, Tp_no = calc_rsrpTsTp(incang, NO_layers, x)
Rglass = np.abs(rs_no) ** 2

# Plot reflectance vs wavelength for different cases
plt.figure()
plt.plot(x, R0, label='R0')
plt.plot(x, Rs40, label='Rs40')
plt.plot(x, Rp40, label='Rp40')
plt.plot(x, Rglass, label='Rglass')
plt.legend()
plt.title('Reflectance vs Wavelength')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

# Calculate adjusted reflectance for 40 degrees incidence angle
cos_ang_fi = np.cos(30 * np.pi / 180)  # Define ang_fi here
sin_ang_fi = np.sin(30 * np.pi / 180)
R40P30 = (Rs40 * sin_ang_fi ** 2 + Rp40 * cos_ang_fi ** 2) / 2
R40Nat = (Rs40 + Rp40) / 2


# Plot adjusted reflectance vs wavelength
plt.figure()
plt.plot(x, R40P30, label='R40P30')
plt.plot(x, R40Nat, label='R40Nat')
plt.legend()
plt.title('Reflectance vs Wavelength (Adjusted)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

# Show plots
plt.show()