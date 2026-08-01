
def nonlin_bc_bc(ya, yb):
    phiA, phipA = ya
    phiC, phipC = yb

    kappa, ioA, ioC, V, f = 1.64, 0.01, 1.0e-4, 0.5, 38.9

    # Butler-Volmer Kinetics at Anode
    hA = 0.0-phiA-0.0
    iA = ioA * (np.exp(f*hA) - np.exp(-f*hA))
    res0 = iA + kappa * phipA

    # Butler-Volmer Kinetics at Cathode
    hC = V - phiC - 1.0
    iC = ioC * (np.exp(f*hC) - np.exp(-f*hC))
    res1 = iC - kappa*phipC

    return np.array([res0, res1])

