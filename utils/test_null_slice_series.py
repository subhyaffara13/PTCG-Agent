
def test_null_slice_series(backend, method):
    _, _, Series = backend
    s = Series([1, 2, 3], index=["a", "b", "c"])
    s_orig = s.copy()

    s2 = method(s)

    # we always return new objects, regardless of CoW or not
    assert s2 is not s
    assert s2.index is not s.index

    # and those trigger CoW when mutated
    s2.iloc[0] = 0
    tm.assert_series_equal(s, s_orig)

