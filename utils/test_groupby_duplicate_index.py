
def test_groupby_duplicate_index():
    # GH#29189 the groupby call here used to raise
    ser = Series([2, 5, 6, 8], index=[2.0, 4.0, 4.0, 5.0])
    gb = ser.groupby(level=0)

    result = gb.mean()
    expected = Series([2, 5.5, 8], index=[2.0, 4.0, 5.0])
    tm.assert_series_equal(result, expected)

