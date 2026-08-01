
def test_series_equal_order_mismatch(check_like):
    s1 = Series([1, 2, 3], index=["a", "b", "c"])
    s2 = Series([3, 2, 1], index=["c", "b", "a"])

    if not check_like:  # Do not ignore index ordering.
        with pytest.raises(AssertionError, match="Series.index are different"):
            tm.assert_series_equal(s1, s2, check_like=check_like)
    else:
        _assert_series_equal_both(s1, s2, check_like=check_like)

