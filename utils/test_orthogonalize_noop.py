
def test_orthogonalize_noop(func, type, norm, xp):
    # Transforms where orthogonalize is a no-op
    x = xp.asarray(np.random.rand(100))
    y1 = func(x, type=type, norm=norm, orthogonalize=True)
    y2 = func(x, type=type, norm=norm, orthogonalize=False)
    xp_assert_close(y1, y2)

