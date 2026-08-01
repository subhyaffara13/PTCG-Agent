
def test_subset_chained_getitem_series(backend, method):
    # Case: creating a subset using multiple, chained getitem calls using views
    # still needs to guarantee proper CoW behaviour
    _, _, Series = backend
    s = Series([1, 2, 3], index=["a", "b", "c"])
    s_orig = s.copy()

    # modify subset -> don't modify parent
    subset = method(s)
    subset.iloc[0] = 0
    tm.assert_series_equal(s, s_orig)

    # modify parent -> don't modify subset
    subset = s.iloc[0:3].iloc[0:2]
    s.iloc[0] = 0
    expected = Series([1, 2], index=["a", "b"])
    tm.assert_series_equal(subset, expected)

