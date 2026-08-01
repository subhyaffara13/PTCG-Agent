
def test_large_unequal_ints(dtype):
    # https://github.com/pandas-dev/pandas/issues/55882
    left = Series([1577840521123000], dtype=dtype)
    right = Series([1577840521123543], dtype=dtype)
    with pytest.raises(AssertionError, match="Series are different"):
        tm.assert_series_equal(left, right)

