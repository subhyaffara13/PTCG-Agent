
def test_inv_boxcox1p_underflow():
    x = 1e-15
    lam = 1e-306
    y = inv_boxcox1p(x, lam)
    assert_allclose(y, x, rtol=1e-14)

