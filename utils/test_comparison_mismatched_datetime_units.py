
def test_comparison_mismatched_datetime_units(index):
    # GH#63459

    ser = Series(1, index=index)
    ser2 = Series(1, index=index.as_unit("ns"))

    result = ser == ser2
    expected = Series([True, True, True], index=ser.index)
    tm.assert_series_equal(result, expected)

    result2 = ser2 < ser
    expected2 = Series([False, False, False], index=ser2.index)
    tm.assert_series_equal(result2, expected2)

