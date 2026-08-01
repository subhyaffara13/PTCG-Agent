
def test_fullmatch_compiled_regex(any_string_dtype):
    # GH#61952
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    values = Series(["ab", "AB", "abc", "ABC"], dtype=any_string_dtype)

    result = values.str.fullmatch(re.compile("ab"))
    expected = Series([True, False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # TODO this currently works for pyarrow-backed dtypes but raises for python
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        result = values.str.fullmatch(re.compile("ab"), case=False)
        expected = Series([True, True, False, False], dtype=expected_dtype)
        tm.assert_series_equal(result, expected)
    else:
        with pytest.raises(
            ValueError, match="cannot process flags argument with a compiled pattern"
        ):
            values.str.fullmatch(re.compile("ab"), case=False)

    result = values.str.fullmatch(re.compile("ab", flags=re.IGNORECASE))
    expected = Series([True, True, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    with pytest.raises(
        ValueError, match="cannot process flags argument with a compiled pattern"
    ):
        values.str.fullmatch(re.compile("ab"), flags=re.IGNORECASE)

