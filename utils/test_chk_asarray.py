
def test_chk_asarray(xp):
    rng = np.random.default_rng(2348923425434)
    x0 = rng.random(size=(2, 3, 4))
    x = xp.asarray(x0)

    axis = 1
    x_out, axis_out = _chk_asarray(x, axis=axis, xp=xp)
    xp_assert_equal(x_out, xp.asarray(x0))
    assert_equal(axis_out, axis)

    axis = None
    x_out, axis_out = _chk_asarray(x, axis=axis, xp=xp)
    xp_assert_equal(x_out, xp.asarray(x0.ravel()))
    assert_equal(axis_out, 0)

    axis = 2
    x_out, axis_out = _chk_asarray(x[0, 0, 0], axis=axis, xp=xp)
    xp_assert_equal(x_out, xp.asarray(np.atleast_1d(x0[0, 0, 0])))
    assert_equal(axis_out, axis)

