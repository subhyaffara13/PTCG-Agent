
def test_transform_series():
    ser = Series([1, 2, 3])
    ser_orig = ser.copy()

    def func(ser):
        ser.iloc[0] = 100
        return ser

    ser.transform(func)
    tm.assert_series_equal(ser, ser_orig)


def test_transform_series(_test_series):
    r = _test_series.resample("20min")
    expected = _test_series.groupby(pd.Grouper(freq="20min")).transform("mean")
    result = r.transform("mean")
    tm.assert_series_equal(result, expected)

