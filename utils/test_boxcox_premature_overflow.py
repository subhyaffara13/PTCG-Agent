
def test_boxcox_premature_overflow(x, lmb):
    # test boxcox & inv_boxcox
    y = boxcox(x, lmb)
    assert np.isfinite(y)
    x_inv = inv_boxcox(y, lmb)
    assert_allclose(x, x_inv)

    # test boxcox1p & inv_boxcox1p
    y1p = boxcox1p(x-1, lmb)
    assert np.isfinite(y1p)
    x1p_inv = inv_boxcox1p(y1p, lmb)
    assert_allclose(x-1, x1p_inv)

