
def test_contains_compiled_regex(any_string_dtype):
    # GH#61942
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    ser = Series(["foo", "bar", "Baz"], dtype=any_string_dtype)

    pat = re.compile("ba.")
    result = ser.str.contains(pat)
    expected = Series([False, True, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # TODO this currently works for pyarrow-backed dtypes but raises for python
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        result = ser.str.contains(pat, case=False)
        expected = Series([False, True, True], dtype=expected_dtype)
        tm.assert_series_equal(result, expected)
    else:
        with pytest.raises(
            ValueError, match="cannot process flags argument with a compiled pattern"
        ):
            ser.str.contains(pat, case=False)

    pat = re.compile("ba.", flags=re.IGNORECASE)
    result = ser.str.contains(pat)
    expected = Series([False, True, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # TODO should this be supported?
    with pytest.raises(
        ValueError, match="cannot process flags argument with a compiled pattern"
    ):
        ser.str.contains(pat, flags=re.IGNORECASE)

