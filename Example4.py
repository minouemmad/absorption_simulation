# -*- coding: utf-8 -*-
from numpy import linspace, pi, sin, arcsin, nan, abs, ones
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, plot, legend, xlabel, ylabel, title
from Funcs import calc_rsrpTsTp, calc_Nlayer

# Define wavelength range in microns
nlamb = 301
x_microns = linspace(0, 15, nlamb)  # from 0 to 15 microns
x = x_microns * 1e3  # convert to nm for calculations

# Define layers for metal structure (Titanium, Platinum, Gold)
layers_metal = [
    [nan, 'Constant', [1.0, 0.0]],  # Air
    [50, 'Drude', [5.75, 2.14, 1.34e13]],  # Titanium layer (thickness 50 nm)
    [30, 'Drude', [9.59, 0.34, 2.0e13]],  # Platinum layer (thickness 30 nm)
    [20, 'Drude', [9.03, 0.51, 1.5e13]],  # Gold layer (thickness 20 nm)
    [nan, 'Constant', [1.0, 0.0]]  # Substrate (assumed to be air for simplicity)
]

# Define layers for semiconductor structure (GaSb, AlSbAs, GaSb)
layers_semiconductor = [
    [nan, 'Constant', [1.0, 0.0]],  # Air
    [100, 'Sellmeier', [5.4, 3.0e4, 0.23]],  # GaSb layer (100 nm)
    [200, 'Cauchy', [2.95, 0.01, 0.0, 0.0, 0.0]],  # AlSbAs layer (200 nm)
    [500, 'Sellmeier', [5.4, 3.0e4, 0.23]],  # GaSb layer (500 nm)
    [nan, 'Constant', [1.0, 0.0]]  # Substrate (assumed to be air for simplicity)
]

# Define incidence angle (in radians)
incang = 10 * pi / 180 * ones(x.size)

# Calculate RTA for metal structure
[rs_metal, rp_metal, Ts_metal, Tp_metal] = calc_rsrpTsTp(incang, layers_metal, x)
Rs_metal = (abs(rs_metal)) ** 2
Rp_metal = (abs(rp_metal)) ** 2
Ts_metal = Ts_metal
Tp_metal = Tp_metal
As_metal = 1 - Rs_metal - Ts_metal  # Absorption for s-polarization
Ap_metal = 1 - Rp_metal - Tp_metal  # Absorption for p-polarization

# Calculate RTA for semiconductor structure
[rs_semiconductor, rp_semiconductor, Ts_semiconductor, Tp_semiconductor] = calc_rsrpTsTp(incang, layers_semiconductor, x)
Rs_semiconductor = (abs(rs_semiconductor)) ** 2
Rp_semiconductor = (abs(rp_semiconductor)) ** 2
Ts_semiconductor = Ts_semiconductor
Tp_semiconductor = Tp_semiconductor
As_semiconductor = 1 - Rs_semiconductor - Ts_semiconductor  # Absorption for s-polarization
Ap_semiconductor = 1 - Rp_semiconductor - Tp_semiconductor  # Absorption for p-polarization

# Updated plotting with descriptive labels
figure()
plot(x_microns, Rs_metal, 'k', label='Reflectance - Metal')
plot(x_microns, Rp_metal, 'r', label='Reflectance (p-pol) - Metal')
plot(x_microns, Rs_semiconductor, 'b', label='Reflectance - Semiconductor')
plot(x_microns, Rp_semiconductor, 'g', label='Reflectance (p-pol) - Semiconductor')
xlabel('Wavelength (microns)')
ylabel('Reflectance Coefficient')
title('Reflectance vs Wavelength')
legend()

figure()
plot(x_microns, Ts_metal, 'k', label='Transmittance - Metal')
plot(x_microns, Tp_metal, 'r', label='Transmittance (p-pol) - Metal')
plot(x_microns, Ts_semiconductor, 'b', label='Transmittance - Semiconductor')
plot(x_microns, Tp_semiconductor, 'g', label='Transmittance (p-pol) - Semiconductor')
xlabel('Wavelength (microns)')
ylabel('Transmittance Coefficient')
title('Transmittance vs Wavelength')
legend()

figure()
plot(x_microns, As_metal, 'k', label='Absorbance - Metal')
plot(x_microns, Ap_metal, 'r', label='Absorbance (p-pol) - Metal')
plot(x_microns, As_semiconductor, 'b', label='Absorbance - Semiconductor')
plot(x_microns, Ap_semiconductor, 'g', label='Absorbance (p-pol) - Semiconductor')
xlabel('Wavelength (microns)')
ylabel('Absorbance Coefficient')
title('Absorbance vs Wavelength')
legend()

figure()
plot(x_microns, Rs_metal, 'k', label='Reflectance - Metal')
plot(x_microns, Rp_metal, 'r', label='Reflectance (p-pol) - Metal')
plot(x_microns, Ts_metal, 'k--', label='Transmittance - Metal')
plot(x_microns, Tp_metal, 'r--', label='Transmittance (p-pol) - Metal')
plot(x_microns, As_metal, 'k:', label='Absorbance - Metal')
plot(x_microns, Ap_metal, 'r:', label='Absorbance (p-pol) - Metal')
xlabel('Wavelength (microns)')
ylabel('RTA Coefficients')
title('RTA vs Wavelength - Metal Structure')
legend()

figure()
plot(x_microns, Rs_semiconductor, 'b', label='Reflectance - Semiconductor')
plot(x_microns, Rp_semiconductor, 'g', label='Reflectance (p-pol) - Semiconductor')
plot(x_microns, Ts_semiconductor, 'b--', label='Transmittance - Semiconductor')
plot(x_microns, Tp_semiconductor, 'g--', label='Transmittance (p-pol) - Semiconductor')
plot(x_microns, As_semiconductor, 'b:', label='Absorbance - Semiconductor')
plot(x_microns, Ap_semiconductor, 'g:', label='Absorbance (p-pol) - Semiconductor')
xlabel('Wavelength (microns)')
ylabel('RTA Coefficients')
title('RTA vs Wavelength - TiPtAu')
legend()

plt.show()