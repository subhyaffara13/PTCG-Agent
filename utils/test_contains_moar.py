
def test_contains_moar(any_string_dtype):
    # PR #1179
    s = Series(
        ["A", "B", "C", "Aaba", "Baca", "", np.nan, "CABA", "dog", "cat"],
        dtype=any_string_dtype,
    )

    result = s.str.contains("a")
    if any_string_dtype == "str":
        # NaN propagates as False
        expected_dtype = bool
        na_value = False
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        na_value = np.nan
    expected = Series(
        [False, False, False, True, True, False, na_value, False, False, True],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = s.str.contains("a", case=False)
    expected = Series(
        [True, False, False, True, True, False, na_value, True, False, True],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = s.str.contains("Aa")
    expected = Series(
        [False, False, False, True, False, False, na_value, False, False, False],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = s.str.contains("ba")
    expected = Series(
        [False, False, False, True, False, False, na_value, False, False, False],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

    result = s.str.contains("ba", case=False)
    expected = Series(
        [False, False, False, True, True, False, na_value, True, False, False],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

