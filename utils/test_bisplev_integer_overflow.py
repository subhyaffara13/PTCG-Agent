
def test_bisplev_integer_overflow():
    np.random.seed(1)

    x = np.linspace(0, 1, 11)
    y = x
    z = np.random.randn(11, 11).ravel()
    kx = 1
    ky = 1

    nx, tx, ny, ty, c, fp, ier = regrid_smth(
        x, y, z, None, None, None, None, kx=kx, ky=ky, s=0.0, maxit=20)
    tck = (tx[:nx], ty[:ny], c[:(nx - kx - 1) * (ny - ky - 1)], kx, ky)

    xp = np.zeros([2621440])
    yp = np.zeros([2621440])

    assert_raises((RuntimeError, MemoryError), bisplev, xp, yp, tck)

