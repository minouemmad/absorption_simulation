import numpy as np
from numpy import linspace, pi, sin, cos, arcsin, nan, abs, ones
import matplotlib.pyplot as plt
from Funcs import calc_rsrpTsTp

# Define the refractive index functions
def sellmeier_equation(params, wavelength):
    B1, B2, B3 = params
    wavelength_m = wavelength * 1e-9  # Convert nm to meters for the formula
    n_squared = B1 + (B2 * wavelength_m**2) / (wavelength_m**2 - B3**2)
    n = np.sqrt(n_squared)
    return n

# Define parameters
nlamb = 31
wavelengths = np.linspace(400, 700, nlamb)

# Refractive index parameters
gaSb_params = [14.10, 0.442, 1503e-9]  # Sellmeier parameters for GaSb
alSbAs_params = [8.82, 0.79, 589e-9]  # Sellmeier parameters for AlSbAs


# Calculate refractive indices for each wavelength
n_gaSb = np.array([sellmeier_equation(gaSb_params, wl) for wl in wavelengths])
n_alSbAs = np.array([sellmeier_equation(alSbAs_params, wl) for wl in wavelengths])

# Plot dispersion model for refractive indices
plt.figure()
plt.plot(wavelengths, n_gaSb, label='GaSb')
plt.plot(wavelengths, n_alSbAs, label='AlSbAs')
plt.legend()
plt.title('Dispersion Model for Refractive Index')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Refractive Index')

# Define layers with refractive indices
layers = [
    [93, "Sellmeier", n_alSbAs],  # AlSbAs
    [121, "Sellmeier", n_gaSb],  # GaSb
    [185, "Sellmeier", n_alSbAs],  # AlSbAs
    [nan, 'Constant', [1.0, 0.0]]  # air
]

# Define incidence angle
incang = np.zeros(wavelengths.size)

# Calculate reflectance for normal incidence
rs, rp, Ts, Tp = calc_rsrpTsTp(incang, layers, wavelengths)
R0 = np.abs(rs) ** 2

# Calculate reflectance for 40 degrees incidence angle
incang_40 = 40 * np.pi / 180 * np.ones(wavelengths.size)
rs_40, rp_40, Ts_40, Tp_40 = calc_rsrpTsTp(incang_40, layers, wavelengths)
Rs40 = np.abs(rs_40) ** 2

# Define layers for no layers case
NO_layers = [
    [np.nan, "Constant", [1., 0.]],
    [np.nan, "BK7", [0]]
]

# Calculate reflectance for no layers
rs_no, rp_no, Ts_no, Tp_no = calc_rsrpTsTp(incang, NO_layers, wavelengths)
Rglass = np.abs(rs_no) ** 2

# Plot reflectance vs wavelength for different cases
plt.figure()
plt.plot(wavelengths, R0, label='AlSbAs/GaSb/AlSbAs Structure')
plt.plot(wavelengths, Rs40, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees)')
plt.plot(wavelengths, Rglass, label='No Layers (BK7)')
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
plt.plot(wavelengths, R40P30, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees, P30)')
plt.plot(wavelengths, R40Nat, label='AlSbAs/GaSb/AlSbAs Structure (40 degrees, Nat)')
plt.legend()
plt.title('Reflectance vs Wavelength (Adjusted)')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflectance')

# Show plots
plt.show()
