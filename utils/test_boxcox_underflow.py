
def test_boxcox_underflow():
    x = 1 + 1e-15
    lmbda = 1e-306
    y = boxcox(x, lmbda)
    assert_allclose(y, np.log(x), rtol=1e-14)

