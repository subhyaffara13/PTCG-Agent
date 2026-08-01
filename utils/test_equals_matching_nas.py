
def test_equals_matching_nas():
    # matching but not identical NAs
    left = Series([np.datetime64("NaT", "ns")], dtype=object)
    right = Series([np.datetime64("NaT", "ns")], dtype=object)
    assert left.equals(right)
    assert Index(left).equals(Index(right))
    assert left.array.equals(right.array)

    left = Series([np.timedelta64("NaT", "ns")], dtype=object)
    right = Series([np.timedelta64("NaT", "ns")], dtype=object)
    assert left.equals(right)
    assert Index(left).equals(Index(right))
    assert left.array.equals(right.array)

    left = Series([np.float64("NaN")], dtype=object)
    right = Series([np.float64("NaN")], dtype=object)
    assert left.equals(right)
    assert Index(left, dtype=left.dtype).equals(Index(right, dtype=right.dtype))
    assert left.array.equals(right.array)

