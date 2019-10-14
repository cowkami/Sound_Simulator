from backend import backend as bd
from backend import set_backend
from matrix_visualizer import MatrixVisualizer

set_backend('torch.cuda.float32')

NX = 500
NY = 300
NZ = 100

dx = 0.01
dt = 20.0e-6

N_STEP = 10000

freq = 1.0e+03

C = 340
rho = 1.2
kappa = C * rho


# PML layer
S_max = 50  # max sigma means maximum attenuation coefficients.
W_PML = 30  # width of perfetly matched layer.
Sx = bd.zeros((NX+1, NY,   NZ))
Sy = bd.zeros((NX,   NY+1, NZ))
Sz = bd.zeros((NX,   NY,   NZ+1))

# set sigma which is increase from the inner boundary
# to the outer of the PML.
S_inc = (dx * bd.arange(0, W_PML, 1.0) / W_PML) * S_max

for i, sigma in enumerate(S_inc, 1):
    Sx[W_PML - i, :, :] = sigma
    Sx[-W_PML + i, :, :] = sigma
    Sy[:, W_PML - i, :] = sigma
    Sy[:, -W_PML + i, :] = sigma
    Sz[:, :, W_PML - i] = sigma
    Sz[:, :, -W_PML + i] = sigma

# set tensor
Vx = bd.zeros((NX+1, NY,   NZ))
Vy = bd.zeros((NX,   NY+1, NZ))
Vz = bd.zeros((NX,   NY,   NZ+1))
P = bd.zeros((NX,   NY,   NZ))


def diff(tensor, axis=0):
    i = [0, 0, 0]
    i[axis] = 1
    Nx, Ny, Nz = tensor.shape
    return (
        tensor[i[0]:, i[1]:, i[2]:] - tensor[:Nx-i[0], :Ny-i[1], :Nz-i[2]])


vis = MatrixVisualizer(4*NX, 4*(NY+NZ))

for n in range(N_STEP+1):
    Vx[1:-1, :, :] -= (dt / (rho * dx)) * (diff(P, axis=0)) \
        + (C * dt) * Sx[1:-1, :, :] * Vx[1:-1, :, :]
    Vy[:, 1:-1, :] -= (dt / (rho * dx)) * (diff(P, axis=1)) \
        + (C * dt) * Sy[:, 1:-1, :] * Vy[:, 1:-1, :]
    Vz[:, :, 1:-1] -= (dt / (rho * dx)) * (diff(P, axis=2)) \
        + (C * dt) * Sz[:, :, 1:-1] * Vz[:, :, 1:-1]

    P -= (kappa * dt / dx) * (
              diff(Vx, axis=0)
            + diff(Vy, axis=1)
            + diff(Vz, axis=2)
            + (dt / dx) * (
                  Sx[1:, :, :] * diff(Vx, axis=0)
                + Sy[:, 1:, :] * diff(Vy, axis=1)
                + Sz[:, :, 1:] * diff(Vz, axis=2)
            )) \
        + (C * dt) * (
              Sx[1:, :, :]
            + Sy[:, 1:, :]
            + Sz[:, :, 1:]
        ) * P

    # input signal
    if n % 500 > 0 and n % 500 < 50:
        amp = 5
        theta = bd.array(2.0 * bd.pi * freq * n * dt)
        sig = amp * bd.sin(theta)
        P[int(NX/4), int(NY*4/11):int(NY*6/11), int(NZ/3):int(NZ*2/3)] = sig

    # obstacle
    P[int(NX/2):int(NX*2/3), int(NY/3):int(NY*2/3), :] *= 0.2

    # visualise update
    vis.update(bd.numpy(bd.cat((P[:, :, int(NZ/2)], P[:, int(NY/3), :]), axis=1)))
