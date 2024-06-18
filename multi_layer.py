# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 21:47:21 2022

@author: dmontealegre
"""

import pylab as py

def trmat(kh,n):
    return py.asarray([[py.cos(kh),       1j*py.sin(kh)/n],\
                       [1j*n*py.sin(kh),  py.cos(kh)]])

wl = 4.55
points = 1000
anl = 2*py.pi/py.linspace(2.5,7.5,points+1)*wl/4
anh = 2*py.pi/py.linspace(2.5,7.5,points+1)*wl/4
# anl = py.linspace(0,py.pi,points+1)
# anh = py.linspace(0,py.pi,points+1)
# anl = py.linspace(0.9,py.pi,points+1)
# anh = py.linspace(0.9,py.pi,points+1)
nl = 3.1335
nh = 3.7156
# nl = 1.3726
# nh = 3.4212

ni = 1#3.7156
nt = 3.7156

per = 22
drift = -0.005

R = py.zeros((len(anl),len(anh)))
Rwl = py.zeros(len(anl))
# Rqw = ((nh**(2*per)*ni-nt*nl**(2*per))/(nh**(2*per)*ni+nt*nl**(2*per)))**2
# print(Rqw*100)

maxR = 0
manl,manh = 0,0
manl2,manh2 = 0,0
for i in range(len(anl)):
    for j in range(len(anh)):
        if not i == j:continue
        M = trmat(anl[i],nl)
        for k in range(per):
            M = py.matmul(trmat(anh[j]*(1+drift*k),nh),py.copy(M))
            M = py.matmul(trmat(anl[i]*(1+drift*k),nl),py.copy(M))
        A = py.real(ni*(M[0,0]))
        B = py.imag(ni*nt*(M[0][1]))
        C = py.imag(M[1][0])
        D = py.real(nt*(M[1][1]))
        R[i][j] = ((A**2+B**2-C**2-D**2)**2+4*((A*C)**2+(B*D)**2-2*A*B*C*D))/\
            (A**2+B**2+C**2+D**2+2*(A*D+B*C))**2
        if R[i][j] > maxR:
            maxR = R[i][j]
            manl,manh = anl[i],anh[j]
        elif R[i][j] == maxR:
            manl2,manh2 = anl[i],anh[j]
        if i == j:
            Rwl[i] = R[i][j]
#     # py.plot(an/py.pi,R*100,color='b',linewidth=3)    
# # py.plot(an2/py.pi,R[50]*100,color='b',linewidth=3)
# py.pcolor(anh/py.pi,anl/py.pi,R*100,vmin=90,vmax=100)
print(maxR*100,manl/py.pi,manh/py.pi,manl2/py.pi,manh2/py.pi)
print(R[int(points/2)][int(points/2)]*100)
# py.axvline(anh[int(points/2)]/py.pi)
# py.axhline(anl[int(points/2)]/py.pi)

py.ylabel("Low index kh ($\pi$)",fontsize=20)
py.xlabel("High index kh ($\pi$)",fontsize=20)
py.tick_params(labelsize=20)
py.tight_layout(True)

# fig, ax = py.subplots(tight_layout=True)
# py.plot(2*py.pi/anl*wl/4,Rwl,linewidth=3,color='grey',label='Diel DBR')
py.plot(2*py.pi/anl*wl/4,Rwl,linewidth=3,color='purple',label='Semi DBR')
# py.plot(2*py.pi/anl*wl/4,Rwl,linewidth=3,color=[py.log(per)/py.log(5),0,0,1],label='%d.5 period'%(per))
py.xlim([2.5,7.5])
py.xlabel('$\lambda$ ($\mu$m)',fontsize=20)
py.ylabel('R (%)',fontsize=20)
py.tick_params(labelsize=20)
py.legend(fontsize=15,loc='lower center')
py.show()