import sys
import numpy as np

NX = 300        # $B6u4V%;%k?t(B X [pixels]
NY = 400        # $B6u4V%;%k?t(B Y [pixels]

dx = 0.01        # $B6u4V9o$_(B [m]
dt = 20.0e-6        # $B;~4V9o$_(B [s]

N_STEP = 10000        # $B7W;;%9%F%C%W?t(B [$B2s(B]

freq = 1.0e3        # $B=i4|GH7A$N<~GH?t(B [Hz]

rho = 1.3            # $BL)EY&Q(B [kg/m^3]
kappa = 142.0e3        # $BBN@QCF@-N(&J(B [Pa]

Vx = np.zeros((NX+1, NY), "float64")        # x$BJ}8~N3;RB.EY(B [m/s]
Vy = np.zeros((NX, NY+1), "float64")        # y$BJ}8~N3;RB.EY(B [m/s]
P = np.zeros((NX, NY), "float64")        # $B2;05(B [Pa]


# $B;vA0=`Hw(B
# waveformfile = open('waveform.txt', 'w')

# $B%a%$%s%k!<%W(B
for n in range(N_STEP+1):

    # $B99?7!J$3$3$,(B FDTD $B$NK\BN!K(B
    # $BN3;RB.EY$N99?7(B
    Vx[1:NX, :] += - (dt / (rho * dx)) * (P[1:NX, :] - P[0:NX-1, :])
    Vy[:, 1:NY] += - (dt / (rho * dx)) * (P[:, 1:NY] - P[:, 0:NY-1])
    # $B2;05$N99?7(B
    P[0:NX, 0:NY] += - (kappa * dt / dx)\
                     * ((Vx[1:NX+1] - Vx[0:NX, :]) + (Vy[:, 1:NY+1] - Vy[:, 0:NY]))

    # $B=i4|GH7A$r=`Hw!J@589GH!_#1GH(B with $B%O%sAk!K(B
    if n < (1.0/freq)/dt:
        sig = ((1.0 - np.cos(2.0 * np.pi * freq * n * dt)) / 2.0) \
              * np.sin(2.0 * np.pi * freq * n * dt)
    else:
        sig = 0.0

    # $B2;8;(B
    P[int(NX/4), int(NY/3)] = sig

    # $BGH7A%U%!%$%k=PNO!J;~9o(B, $B2;8;(B, $BCf1{E@$N2;05!K(B
    # waveformfile.write('%e\t%e\t%e\n' % (dt*n, sig, P[int(NX/2),int(NY/2)]))

    # $B2;05J,I[%U%!%$%k=PNO!J(B50$B%9%F%C%WKh!K(B
    if n % 50 == 0:
        sys.stderr.write('%5d / %5d\r' % (n, N_STEP))
#        $B2;>l%U%!%$%k$r=PNO$9$k>l9g$O0J2<$N%3%a%s%H$r30$7$F2<$5$$(B
        fieldfilename = 'field%.6d.txt' % (n)
        fieldfile = open(fieldfilename, 'w')
        for i in range(NX):
            for j in range(NY):
                fieldfile.write('%e\t' % (P[i, j]))
            fieldfile.write('\n')
        fieldfile.close

# $B;v8e=hM}(B #########################################################
# waveformfile.close
