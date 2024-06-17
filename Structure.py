import numpy as np
from numpy import linspace, pi, sin, cos, arcsin, nan, abs, ones
import matplotlib.pyplot as plt
from Funcs import calc_rsrpTsTp

# Define parameters
nlamb = 31
x = np.linspace(2000, 10000, nlamb)

# Define layers
layers = [
    
    [20, "Drude", [1.3718831e+16, 0.053, 0]], #Au
    [239, "Sellmeier", [8.82, 0.79, 589e-9]],  # AlSbAs
    [201, "Sellmeier", [14.10, 0.442, 1503e-9]],  # GaSb
    [239, "Sellmeier", [8.82, 0.79, 589e-9]],  # AlSbAs
    [nan, 'Constant', [1.0, 0.0]]  # air
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
plt.plot(x, R0, label='AlSbAs/GaSb/AlSbAs Structure (normal incidence)')
plt.plot(x, Rs40, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees)')
# plt.plot(x, Rglass, label='No Layers (BK7)')
plt.legend()
plt.title('Reflectance vs Wavelength')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

# Calculate adjusted reflectance for 40 degrees incidence angle
cos_ang_fi = np.cos(30 * np.pi / 180)  # Define ang_fi here
sin_ang_fi = np.sin(30 * np.pi / 180)
R40P30 = Rs40 * sin_ang_fi ** 2 / 2
R40Nat = Rs40 / 2

# Plot adjusted reflectance vs wavelength
plt.figure()
plt.plot(x, R40P30, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees, P30)')
# plt.plot(x, R40Nat, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees, Nat)')
plt.legend()
plt.title('Reflectance vs Wavelength (Adjusted)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

# Show plots
plt.show()
