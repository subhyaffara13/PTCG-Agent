
def test_loggamma_taylor():
    # Test around the zeros at z = 1, 2.

    r = np.logspace(-16, np.log10(LOGGAMMA_TAYLOR_RADIUS), 10)
    theta = np.linspace(0, 2*np.pi, 20)
    r, theta = np.meshgrid(r, theta)
    dz = r*np.exp(1j*theta)
    z = np.r_[1 + dz, 2 + dz].flatten()

    dataset = [(z0, complex(mpmath.loggamma(z0))) for z0 in z]
    dataset = np.array(dataset)

    FuncData(sc.loggamma, dataset, 0, 1, rtol=5e-14).check()

