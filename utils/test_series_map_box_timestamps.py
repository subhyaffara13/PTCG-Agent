
def test_series_map_box_timestamps():
    # GH#2689, GH#2627
    ser = Series(date_range("1/1/2000", periods=3))

    def func(x):
        return (x.hour, x.day, x.month)

    result = ser.map(func)
    expected = Series([(0, 1, 1), (0, 2, 1), (0, 3, 1)])
    tm.assert_series_equal(result, expected)

