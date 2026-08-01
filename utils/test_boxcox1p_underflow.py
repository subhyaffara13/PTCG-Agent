
def test_boxcox1p_underflow():
    x = np.array([1e-15, 1e-306])
    lmbda = np.array([1e-306, 1e-18])
    y = boxcox1p(x, lmbda)
    assert_allclose(y, np.log1p(x), rtol=1e-14)

