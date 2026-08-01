
def test_duplicated_nan_none(keep, expected):
    ser = Series([np.nan, 3, 3, None, np.nan], dtype=object)

    result = ser.duplicated(keep=keep)
    expected = Series(expected)
    tm.assert_series_equal(result, expected)


def test_duplicated_nan_none(keep, expected):
    df = DataFrame({"C": [np.nan, 3, 3, None, np.nan], "x": 1}, dtype=object)

    result = df.duplicated(keep=keep)
    tm.assert_series_equal(result, expected)

