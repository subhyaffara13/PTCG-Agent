
def test_inv_boxcox():
    x = np.array([0., 1., 2.])
    lam = np.array([0., 1., 2.])
    y = boxcox(x, lam)
    x2 = inv_boxcox(y, lam)
    assert_allclose(x, x2, atol=1.5e-7, rtol=0)

    x = np.array([0., 1., 2.])
    lam = np.array([0., 1., 2.])
    y = boxcox1p(x, lam)
    x2 = inv_boxcox1p(y, lam)
    assert_allclose(x, x2, atol=1.5e-7, rtol=0)

