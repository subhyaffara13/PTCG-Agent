
def test_chdtr_gh21311(xp):
    # the edge case behavior of generic chdtr was not right; see gh-21311
    # be sure to test at least these cases
    # should add `np.nan` into the mix when gh-21317 is resolved
    x = np.asarray([-np.inf, -1., 0., 1., np.inf])
    v = x.reshape(-1, 1)
    ref = special.chdtr(v, x)
    res = special.chdtr(xp.asarray(v), xp.asarray(x))
    xp_assert_close(res, xp.asarray(ref))

