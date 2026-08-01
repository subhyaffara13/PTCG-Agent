
def test_drop_duplicates_no_duplicates(any_numpy_dtype, keep, values):
    tc = Series(values, dtype=np.dtype(any_numpy_dtype))
    expected = Series([False] * len(tc), dtype="bool")

    if tc.dtype == "bool":
        # 0 -> False and 1-> True
        # any other value would be duplicated
        tc = tc[:2]
        expected = expected[:2]

    tm.assert_series_equal(tc.duplicated(keep=keep), expected)

    result_dropped = tc.drop_duplicates(keep=keep)
    tm.assert_series_equal(result_dropped, tc)

    # validate shallow copy
    assert result_dropped is not tc

