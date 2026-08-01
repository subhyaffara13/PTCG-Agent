
def test_orthogonalize_dcst2(func, norm, xp):
    x = xp.asarray(np.random.rand(100))
    y1 = func(x, type=2, norm=norm, orthogonalize=True)
    y2 = func(x, type=2, norm=norm, orthogonalize=False)

    xpx.at(y2, 0 if func.__name__ == "dct" else -1).divide(SQRT_2)
    xp_assert_close(y1, y2)

