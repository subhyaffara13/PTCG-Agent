
def test_contains_na_kwarg_for_nullable_string_dtype(
    nullable_string_dtype, na, expected, regex
):
    # https://github.com/pandas-dev/pandas/pull/41025#issuecomment-824062416

    values = Series(["a", "b", "c", "a", np.nan], dtype=nullable_string_dtype)

    if na in [0, 3] and na is not False:
        msg = f"na must be None, pd.NA, np.nan, True, or False; got {na}"
        with pytest.raises(ValueError, match=msg):
            values.str.contains("a", na=na, regex=regex)
    else:
        result = values.str.contains("a", na=na, regex=regex)
        expected = Series([True, False, False, True, expected], dtype="boolean")
        tm.assert_series_equal(result, expected)

