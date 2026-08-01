
def test_to_numeric_from_nullable_string_coerce(nullable_string_dtype):
    # GH#52146
    values = ["a", "1"]
    ser = Series(values, dtype=nullable_string_dtype)
    result = to_numeric(ser, errors="coerce")
    expected = Series([pd.NA, 1], dtype="Int64")
    tm.assert_series_equal(result, expected)

