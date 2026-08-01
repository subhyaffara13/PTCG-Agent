
def test_series_getitem_slice(backend):
    # Case: taking a slice of a Series + afterwards modifying the subset
    _, _, Series = backend
    s = Series([1, 2, 3], index=["a", "b", "c"])
    s_orig = s.copy()

    subset = s[:]
    assert np.shares_memory(get_array(subset), get_array(s))
    assert subset.index is not s.index

    subset.iloc[0] = 0

    assert not np.shares_memory(get_array(subset), get_array(s))

    expected = Series([0, 2, 3], index=["a", "b", "c"])
    tm.assert_series_equal(subset, expected)

    # original parent series is not modified (CoW)
    tm.assert_series_equal(s, s_orig)

