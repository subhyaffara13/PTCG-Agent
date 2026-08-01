
def test_series_map_box_timedelta(by_row):
    # GH#11349
    ser = Series(timedelta_range("1 day 1 s", periods=3, freq="h"))

    def f(x):
        return x.total_seconds() if by_row else x.dt.total_seconds()

    result = ser.apply(f, by_row=by_row)

    expected = ser.map(lambda x: x.total_seconds())
    tm.assert_series_equal(result, expected)

    expected = Series([86401.0, 90001.0, 93601.0])
    tm.assert_series_equal(result, expected)


def test_series_map_box_timedelta():
    # GH#11349
    ser = Series(timedelta_range("1 day 1 s", periods=5, freq="h"))

    def f(x):
        return x.total_seconds()

    ser.map(f)

