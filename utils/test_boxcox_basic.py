
def test_boxcox_basic():
    x = np.array([0.5, 1, 2, 4])

    # lambda = 0  =>  y = log(x)
    y = boxcox(x, 0)
    assert_allclose(y, np.log(x), atol=1.5e-7, rtol=0)

    # lambda = 1  =>  y = x - 1
    y = boxcox(x, 1)
    assert_allclose(y, x - 1, atol=1.5e-7, rtol=0)

    # lambda = 2  =>  y = 0.5*(x**2 - 1)
    y = boxcox(x, 2)
    assert_allclose(y, 0.5*(x**2 - 1), atol=1.5e-7, rtol=0)

    # x = 0 and lambda > 0  =>  y = -1 / lambda
    lam = np.array([0.5, 1, 2])
    y = boxcox(0, lam)
    assert_allclose(y, -1.0 / lam, atol=1.5e-7, rtol=0)

