
def test_contains_nan(any_string_dtype):
    # PR #14171
    s = Series([np.nan, np.nan, np.nan], dtype=any_string_dtype)

    result = s.str.contains("foo", na=False)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series([False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = s.str.contains("foo", na=True)
    expected = Series([True, True, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    msg = "na must be None, pd.NA, np.nan, True, or False; got foo"
    with pytest.raises(ValueError, match=msg):
        s.str.contains("foo", na="foo")

    result = s.str.contains("foo")
    if any_string_dtype == "str":
        # NaN propagates as False
        expected = Series([False, False, False], dtype=bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series([np.nan, np.nan, np.nan], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)


def test_contains_nan(using_nan_is_na):
    # GH#52840
    arr = pd.array(range(5)) / 0

    assert np.isnan(arr._data[0])
    if using_nan_is_na:
        assert arr.isna()[0]
    else:
        assert not arr.isna()[0]
    assert np.nan in arr

