
def test_spence_circle():
    # The trickiest region for spence is around the circle |z - 1| = 1,
    # so test that region carefully.

    def spence(z):
        return complex(mpmath.polylog(2, 1 - z))

    r = np.linspace(0.5, 1.5)
    theta = np.linspace(0, 2*pi)
    z = (1 + np.outer(r, np.exp(1j*theta))).flatten()
    dataset = np.asarray([(z0, spence(z0)) for z0 in z])

    FuncData(sc.spence, dataset, 0, 1, rtol=1e-14).check()

