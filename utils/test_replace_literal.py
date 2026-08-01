
def test_replace_literal(regex, expected_val, any_string_dtype):
    # GH16808 literal replace (regex=False vs regex=True)
    ser = Series(["f.o", "foo", np.nan], dtype=any_string_dtype)
    expected = Series(["bao", expected_val, np.nan], dtype=any_string_dtype)
    result = ser.str.replace("f.", "ba", regex=regex)
    tm.assert_series_equal(result, expected)

