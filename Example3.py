# Example3.py
# The third example illustrates how our computational 
# procedures are able to address specialized research topics by 
# simple adaptations of our codes.

# -*- coding: utf-8 -*-
from numpy import *
from matplotlib.pyplot import *
from Funcs import *

layers = [
    [nan, "Constant", [1.5,0.]],
    [30, "Constant", [0.056206,4.2776]],
    [nan, "Constant", [1.,0.]]
]

x = linspace(633., 633, 1)
numang = 1000
Rs = zeros(numang, dtype=cfloat)
Rp = zeros(numang, dtype=cfloat)
angles = linspace(0, 90, numang) * pi / 180

cont = 0
for incang in angles:
    [rs, rp, Ts, Tp] = calc_rsrpTsTp(incang, layers, x)
    Rs[cont] = abs(rs)**2
    Rp[cont] = abs(rp)**2
    cont += 1

figure()
plot(angles*180/pi, Rs, label='Rs')
plot(angles*180/pi, Rp, label='Rp')
xlabel('incidence angle (deg)')
ylabel('Reflectance')
legend()

numang = 150
angles = linspace(35, 50, numang) * pi / 180
numthk = 100
thicks = linspace(0, 100, numthk)
Rp = zeros([numthk, numang], dtype=float)

cont = 0
for incang in angles:
    for ithk in range(0, numthk):
        layers[1][0] = thicks[ithk]
        [rs, rp, Ts, Tp] = calc_rsrpTsTp(incang, layers, x)
        Rp[ithk, cont] = abs(rp)**2
    cont += 1

figure()
c = pcolor(angles*180/pi, thicks, Rp, cmap='jet')
colorbar(c, orientation='vertical')
xlabel('incidence angle (deg)')
ylabel('thickness')

layers = [
    [nan, "Constant", [1.5, 0.]],
    [50, "Constant", [0.056206, 4.2776]],
    [nan, "Constant", [1., 0.]]
]

numang = 200
angles = linspace(40, 90, numang) * pi / 180
numnout = 100
nout = linspace(1.0, 1.5, numnout)
Rp = zeros([numnout, numang], dtype=float)

cont = 0
for incang in angles:
    for inou in range(0, numnout):
        layers[2][2][0] = nout[inou]
        [rs, rp, Ts, Tp] = calc_rsrpTsTp(incang, layers, x)
        Rp[inou, cont] = abs(rp)**2
    cont += 1

figure()
c = pcolor(angles*180/pi, nout, Rp, cmap='jet')
colorbar(c, orientation='vertical')
xlabel('incidence angle (deg)')
ylabel('air side refractive index')

show()