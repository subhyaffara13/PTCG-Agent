
def test_numeric(kwargs):
    data = [1, -3.14, 7]

    ser = Series(data, **kwargs)
    result = to_numeric(ser)

    expected = Series(data)
    tm.assert_series_equal(result, expected)

