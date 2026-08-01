
def test_series_getitem_ellipsis():
    # Case: taking a view of a Series using Ellipsis + afterwards modifying the subset
    s = Series([1, 2, 3])
    s_orig = s.copy()

    subset = s[...]
    assert np.shares_memory(get_array(subset), get_array(s))
    assert subset.index is not s.index

    subset.iloc[0] = 0

    assert not np.shares_memory(get_array(subset), get_array(s))

    expected = Series([0, 2, 3])
    tm.assert_series_equal(subset, expected)

    # original parent series is not modified (CoW)
    tm.assert_series_equal(s, s_orig)

