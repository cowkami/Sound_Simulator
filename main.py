# from time import sleep
from backend import backend as bd
from backend import set_backend
from matrix_visualizer import MatrixVisualizer

set_backend('torch.cuda')

NX = 500
NY = 300
NZ = 100

dx = 0.01
dt = 20.0e-6

N_STEP = 10000

freq = 1.0e+03

rho = 13
kappa = 142.0e3

Vx = bd.zeros((NX+1, NY,   NZ))
Vy = bd.zeros((NX,   NY+1, NZ))
Vz = bd.zeros((NX,   NY,   NZ+1))
P = bd.zeros((NX,   NY,   NZ))

vis = MatrixVisualizer(1920, int(NY*1920/(NY+NZ)))

max_ = 0
for n in range(N_STEP+1):
    Vx[1:-1, :, :] -= (dt / (rho * dx)) * (P[1:, :, :] - P[:-1, :, :])
    Vy[:, 1:-1, :] -= (dt / (rho * dx)) * (P[:, 1:, :] - P[:, :-1, :])
    Vz[:, :, 1:-1] -= (dt / (rho * dx)) * (P[:, :, 1:] - P[:, :, :-1])
    P[:NX, :NY, :NZ] -= (kappa * dt / dx) * (
        (Vx[1:, :, :] - Vx[:-1, :, :]) +
        (Vy[:, 1:, :] - Vy[:, :-1, :]) +
        (Vz[:, :, 1:] - Vz[:, :, :-1])
    )
    if n % 500 > 0 and n % 500 < 50:
        amp = 10
        theta = bd.array(2.0 * bd.pi * freq * n * dt)
        sig = amp * ((1.0 - bd.cos(theta)) / 2.0) * bd.sin(theta)
    else:
        sig = 0.0

    P[int(NX/4), int(NY*4/11):int(NY*6/11), int(NZ/3):int(NZ*2/3)] = sig

    # obstacle
    P[int(NX/2):int(NX*2/3), int(NY/3):int(NY*2/3), :] *= 0.2

    vis.update(bd.numpy(bd.cat((P[:, :, int(NZ/2)], P[:, int(NY/3), :]), axis=1)))
#    sleep(.005)