# -*- coding: utf-8 -*-
from numpy import linspace, pi, sin, arcsin, nan, abs, ones
from matplotlib.pyplot import figure, plot, legend
from Funcs import calc_rsrpTsTp, calc_Nlayer

# Define wavelength range
nlamb = 31
x = linspace(400, 700, nlamb)

# Define the layers for structure a and b
layers_a = [
    [nan, 'Constant', [1.0, 0.0]],
    [200, 'Sellmeier', [1.7, 10000]],
    [30, 'Cauchy', [1.5, 10000.0, 0.0, 0.1, 150.0]],
    [nan, 'BK7', [0]]
]

layers_b = [
    [nan, 'BK7', [0]],
    [300, 'Cauchy', [1.8, 10000.0, 0.0, 0.0, 0.0]],
    [30, 'File', ['EMA3_n_k.dat']],
    [nan, 'Constant', [1.0, 0.0]]
]

# Define incidence angle (in radians)
incang = 10 * pi / 180 * ones(x.size)

# Calculate reflection and transmission for structure a
[rs, rp, Ts, Tp] = calc_rsrpTsTp(incang, layers_a, x)
Rs_aPlus = (abs(rs)) ** 2
Rp_aPlus = (abs(rp)) ** 2
Ts_aPlus = Ts
Tp_aPlus = Tp

# Calculate for the inverse of structure a
layers_ainv = layers_a[::-1]  # Reverse layers_a

# Calculate refractive index for layer 0 and its inverse
N0 = calc_Nlayer(layers_a, x, 0)
N0_inv = calc_Nlayer(layers_ainv, x, 0)

# Calculate inverse incidence angle
incang_inv = arcsin(N0 * sin(incang) / N0_inv)

# Reflection and transmission for inverse structure a
[rs, rp, Ts, Tp] = calc_rsrpTsTp(incang_inv, layers_ainv, x)
Rs_aMinus = (abs(rs)) ** 2
Rp_aMinus = (abs(rp)) ** 2
Ts_aMinus = Ts
Tp_aMinus = Tp

# Reflection and transmission for structure b
[rs, rp, Ts, Tp] = calc_rsrpTsTp(incang_inv, layers_b, x)
Rs_bPlus = (abs(rs)) ** 2
Rp_bPlus = (abs(rp)) ** 2
Ts_bPlus = Ts
Tp_bPlus = Tp

# Combined reflection and transmission calculations
Rs = (Rs_aPlus + Rs_bPlus * (Ts_aPlus ** 2 - Rs_aMinus * Rs_bPlus)) / (1 - Rs_aMinus * Rs_bPlus)
Rp = (Rp_aPlus + Rp_bPlus * (Tp_aPlus ** 2 - Rp_aMinus * Rp_bPlus)) / (1 - Rp_aMinus * Rp_bPlus)
Ts = (Ts_aPlus * Ts_bPlus) / (1 - Rs_aMinus * Rs_bPlus)
Tp = (Tp_aPlus * Tp_bPlus) / (1 - Rp_aMinus * Rp_bPlus)

# Plotting the results
figure()
plot(x, Rs, 'k', label='Rs')
plot(x, Rs_aPlus, 'k:', label='Rsa')
plot(x, Rp, 'r', label='Rp')
plot(x, Rp_aPlus, 'r:', label='Rpa')
legend()

figure()
plot(x, Ts_aPlus, label='TsaP')
plot(x, Ts_aMinus, label='TsaM')
plot(x, Tp_aPlus, label='TpaP')
plot(x, Tp_aMinus, label='TpaM')
legend()
