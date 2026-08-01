
def test_digamma_boundary():
    # Check that there isn't a jump in accuracy when we switch from
    # using the asymptotic series to the reflection formula.

    x = -np.logspace(300, -30, 100)
    y = np.array([-6.1, -5.9, 5.9, 6.1])
    x, y = np.meshgrid(x, y)
    z = (x + 1j*y).flatten()

    with mpmath.workdps(30):
        dataset = [(z0, complex(mpmath.digamma(z0))) for z0 in z]
    dataset = np.asarray(dataset)

    FuncData(sc.digamma, dataset, 0, 1, rtol=1e-13).check()

