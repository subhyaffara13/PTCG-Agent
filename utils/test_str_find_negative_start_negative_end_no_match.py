
def test_str_find_negative_start_negative_end_no_match():
    # GH 56791
    ser = pd.Series(["abcdefg", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.find(sub="d", start=-3, end=-6)
    expected = pd.Series([-1, None], dtype=ArrowDtype(pa.int64()))
    tm.assert_series_equal(result, expected)

