
def test_align_stringindex(any_string_dtype):
    left = Series(range(3), index=pd.Index(["a", "b", "d"], dtype=any_string_dtype))
    right = Series(range(3), index=pd.Index(["a", "b", "c"], dtype=any_string_dtype))
    result_left, result_right = left.align(right)

    expected_idx = pd.Index(["a", "b", "c", "d"], dtype=any_string_dtype)
    expected_left = Series([0, 1, np.nan, 2], index=expected_idx)
    expected_right = Series([0, 1, 2, np.nan], index=expected_idx)

    tm.assert_series_equal(result_left, expected_left)
    tm.assert_series_equal(result_right, expected_right)

