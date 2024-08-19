# -*- coding: utf-8 -*-
from numpy import *
from matplotlib.pyplot import *
import Funcs as MF  # import transfer-matrix method (may have to change)
import matplotlib.pyplot as plt

# Refractive indices of materials (assumed constant for simplicity)
GaSb_n = 3.816
Au_n = 6.8         # @ 7 microns k = 41.6, "Refractive index of optical materials in IR region" A.J. Moses, pg. 8-15  
GaAs_n = 3.9476
AlAsSb_n = 3.101

# Refractive indices for GaSb and AlAsSb layers (constant approximation)
GaSb_ln = [3.816, 0.]
AlAsSb_ln = [3.101, 0.]

d_des = 7800  # Not used in current script

# Sellmeier coefficients for refractive index dispersion (not used in current script)
GaSb_sn = [14.10, 0.442, 1503e-9]  # J. Appl. Phys. 84, 4517–4524 (1998) https://doi.org/10.1063/1.368677
AlAsSb_sn = [8.82, 0.79, 589e-9]   # Journal of Applied Physics 94, 5041 (2003); doi: 10.1063/1.1611290

# Layer definitions: [thickness (nm), type of formula, [parameters for formula]]
L_amb = [[nan, "Constant", [1., 0.]]]
L_Au = [[100, "Constant", [0.55, 20.43]]]  # Gold layer
L_Ti = [[20, "Constant", [4.56, 5.96]]]    # Titanium layer
L_Au_LD = [[100, "Lorentz-Drude", ['Au']]]  # Lorentz-Drude model for gold

# Define a 12-period DBR stack of alternating GaSb and AlAsSb layers
L_1262_cav = 12 * [[201., "Constant", GaSb_ln], [239., "Constant", AlAsSb_ln]]

L_AntiR = [[3000 / (4 * sqrt(3.81)), "Constant", [1.95, 0.0]]]  # Anti-reflective layer
L_1262_sub = [[nan, "Constant", GaSb_ln]]  # Substrate layer

# Layer stacks for different configurations
Ls_1262 = L_amb + L_1262_cav + L_1262_sub
Ls_1262_metal = L_amb + L_Au_LD + [[239., "Constant", AlAsSb_ln]] + L_1262_cav + L_1262_sub
Ls_1262_metal = Ls_1262_metal[::-1]

# Substrate
Ls_new = (L_amb + 
          L_1262_sub)
Ls_new = Ls_new[::-1]

# Insert function parameters
nlamb = 3500
x = linspace(500, 7000, nlamb)  # Wavelength range for calculation
incang = 0 * pi / 180 * ones(x.size)  # Incident angle (normal incidence)

# Calculate reflectance for the original stack
[rs, rp, Ts, Tp] = MF.calc_rsrpTsTp(incang, Ls_1262_metal, x)
R0 = (abs(rs))**2
R_1 = 0.33 + 0.67 * R0
T0 = real(Ts)
Abs1 = 1. - R0 - T0

# Calculate reflectance for the new stack
[rs_new, rp_new, Ts_new, Tp_new] = MF.calc_rsrpTsTp(incang, Ls_new, x)
R0_new = (abs(rs_new))**2
R_1_new = 0.33 + 0.67 * R0_new
T0_new = real(Ts_new)
Abs1_new = 1. - R0_new - T0_new

#### Initialize plot ####

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot for the original stack
ax1.plot(x, R0, label='$Original\ Stack$')
ax1.set_xlabel('wavelength (nm)', size=14)
ax1.set_ylabel('Reflectance', size=14)
ax1.set_title('Semi-infinite Sub.(Gold Layer)', size=16)
ax1.legend()
ax1.grid(alpha=0.2)

# Plot for the new stack
ax2.plot(x, R0_new, label='$GaSb$', color='orange')
ax2.set_xlabel('wavelength (nm)', size=14)
ax2.set_ylabel('Reflectance', size=14)
ax2.set_title('Substrate', size=16)
ax2.legend()
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()