
def test_rgamma_zeros():
    # Test around the zeros at z = 0, -1, -2, ...,  -169. (After -169 we
    # get values that are out of floating point range even when we're
    # within 0.1 of the zero.)

    # Can't use too many points here or the test takes forever.
    dx = np.r_[-np.logspace(-1, -13, 3), 0, np.logspace(-13, -1, 3)]
    dy = dx.copy()
    dx, dy = np.meshgrid(dx, dy)
    dz = dx + 1j*dy
    zeros = np.arange(0, -170, -1).reshape(1, 1, -1)
    z = (zeros + np.dstack((dz,)*zeros.size)).flatten()
    with mpmath.workdps(100):
        dataset = [(z0, complex(mpmath.rgamma(z0))) for z0 in z]

    dataset = np.array(dataset)
    FuncData(sc.rgamma, dataset, 0, 1, rtol=1e-12).check()

