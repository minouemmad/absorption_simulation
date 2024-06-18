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
wavelengths = np.linspace(206.6, 826.6, nlamb)

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

plt.show()
