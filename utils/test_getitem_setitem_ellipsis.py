
def test_getitem_setitem_ellipsis():
    s = Series(np.random.default_rng(2).standard_normal(10))

    result = s[...]
    tm.assert_series_equal(result, s)

