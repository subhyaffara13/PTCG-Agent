
def test_cospi_zeros():
    eps = np.finfo(float).eps
    dx = np.r_[-np.logspace(0, -13, 3), 0, np.logspace(-13, 0, 3)]
    dy = dx.copy()
    dx, dy = np.meshgrid(dx, dy)
    dz = dx + 1j*dy
    zeros = (np.arange(-100, 100, 1) + 0.5).reshape(1, 1, -1)
    z = (zeros + np.dstack((dz,)*zeros.size)).flatten()
    dataset = np.asarray([(z0, complex(mpmath.cospi(z0)))
                          for z0 in z])

    FuncData(_cospi, dataset, 0, 1, rtol=2*eps).check()

