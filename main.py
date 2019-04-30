from time import sleep
import numpy as np
from matrix_visualizer import MatrixVisualizer

NX = 300
NY = 400

dx = 0.01
dt = 20.0e-6

N_STEP = 10000

freq = 1.0e+03

rho = 1.3
kappa = 142.0e3

Vx = np.zeros((NX+1, NY), "float64")
Vy = np.zeros((NX, NY+1), "float64")
P = np.zeros((NX, NY), "float64")

v = MatrixVisualizer(NY*3, NX*3)

max_ = 0
for n in range(N_STEP+1):
    Vx[1:-1, :] += - (dt / (rho * dx)) * (P[1:, :] - P[:-1, :])
    Vy[:, 1:-1] += - (dt / (rho * dx)) * (P[:, 1:] - P[:, :-1])
    P[:NX, :NY] += - (kappa * dt / dx) * ((Vx[1:] - Vx[:-1, :])
                   + (Vy[:, 1:] - Vy[:, :-1]))

#    if n < (1.0/freq)/dt:
#    if True:
    if n % 1000 > 0 and n % 1000 < 50:
        sig = ((1.0 - np.cos(2.0 * np.pi * freq * n * dt)) / 2.0) \
              * np.sin(2.0 * np.pi * freq * n * dt)
    else:
        sig = 0.0

    if max_ < P.max():
        max_ = P.max()
        v.value_range_max = max_

    P[int(NX/4), int(NY/3)] = sig

    v.update(P)
    sleep(.005)
