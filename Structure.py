import numpy as np
from numpy import linspace, pi, sin, cos, arcsin, nan, abs, ones
import matplotlib.pyplot as plt
from Funcs import calc_rsrpTsTp

# Define parameters
nlamb = 31
x = np.linspace(2000, 10000, nlamb)

# Define layers
layers = [
    
    [100, "Drude", [2.180, 11.690, 1.1]], #TiPtAu
    [239, "Sellmeier", [8.82, 0.79, 589e-9]],  # AlSbAs
    [201, "Sellmeier", [14.10, 0.442, 1503e-9]],  # GaSb J. Appl. Phys. 84, 4517–4524 (1998) https://doi.org/10.1063/1.368677
    [239, "Sellmeier", [8.82, 0.79, 589e-9]],  # AlSbAs Journal of Applied Physics 94, 5041 (2003); doi: 10.1063/1.1611290
    [nan, "Constant", [1.000277, 0]] #air
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


# Plot reflectance vs wavelength for different cases
plt.figure()
plt.plot(x, R0, label='AlSbAs/GaSb/AlSbAs Structure (normal incidence)')
plt.plot(x, Rs40, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees)')
plt.legend()
plt.title('Reflectance vs Wavelength')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

plt.show()
