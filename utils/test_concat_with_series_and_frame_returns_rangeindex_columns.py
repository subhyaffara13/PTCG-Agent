
def test_concat_with_series_and_frame_returns_rangeindex_columns():
    ser = Series([0])
    df = DataFrame([1, 2])
    result = concat([ser, df])
    expected = DataFrame([0, 1, 2], index=[0, 0, 1])
    tm.assert_frame_equal(result, expected, check_column_type=True)

