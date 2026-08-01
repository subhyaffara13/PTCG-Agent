
def test_orthogonalize_dct1(norm, xp):
    x = xp.asarray(np.random.rand(100))

    x2 = xp_copy(x, xp=xp)
    xpx.at(x2, 0).multiply(SQRT_2)
    xpx.at(x2, -1).multiply(SQRT_2)

    y1 = dct(x, type=1, norm=norm, orthogonalize=True)
    y2 = dct(x2, type=1, norm=norm, orthogonalize=False)

    xpx.at(y2, 0).divide(SQRT_2)
    xpx.at(y2, -1).divide(SQRT_2)
    xp_assert_close(y1, y2)

