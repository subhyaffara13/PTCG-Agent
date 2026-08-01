
def test_orthogonalize_dcst3(func, norm, xp):
    x = xp.asarray(np.random.rand(100))
    x2 = xp_copy(x, xp=xp)
    xpx.at(x2, 0 if func.__name__ == "dct" else -1).multiply(SQRT_2)

    y1 = func(x, type=3, norm=norm, orthogonalize=True)
    y2 = func(x2, type=3, norm=norm, orthogonalize=False)
    xp_assert_close(y1, y2)

