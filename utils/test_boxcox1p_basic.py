
def test_boxcox1p_basic():
    x = np.array([-0.25, -1e-20, 0, 1e-20, 0.25, 1, 3])

    # lambda = 0  =>  y = log(1+x)
    y = boxcox1p(x, 0)
    assert_allclose(y, np.log1p(x), atol=1.5e-7, rtol=0)

    # lambda = 1  =>  y = x
    y = boxcox1p(x, 1)
    assert_allclose(y, x, atol=1.5e-7, rtol=0)

    # lambda = 2  =>  y = 0.5*((1+x)**2 - 1) = 0.5*x*(2 + x)
    y = boxcox1p(x, 2)
    assert_allclose(y, 0.5*x*(2 + x), atol=1.5e-7, rtol=0)

    # x = -1 and lambda > 0  =>  y = -1 / lambda
    lam = np.array([0.5, 1, 2])
    y = boxcox1p(-1, lam)
    assert_allclose(y, -1.0 / lam, atol=1.5e-7, rtol=0)

