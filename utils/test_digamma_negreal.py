
def test_digamma_negreal():
    # Test digamma around the negative real axis. Don't do this in
    # TestSystematic because the points need some jiggering so that
    # mpmath doesn't take forever.

    digamma = exception_to_nan(mpmath.digamma)

    x = -np.logspace(300, -30, 100)
    y = np.r_[-np.logspace(0, -3, 5), 0, np.logspace(-3, 0, 5)]
    x, y = np.meshgrid(x, y)
    z = (x + 1j*y).flatten()

    with mpmath.workdps(40):
        dataset = [(z0, complex(digamma(z0))) for z0 in z]
    dataset = np.asarray(dataset)

    FuncData(sc.digamma, dataset, 0, 1, rtol=1e-13).check()

