
def test_resample_entirely_nat_window(method, method_args, unit):
    ser = Series([0] * 2 + [np.nan] * 2, index=date_range("2017", periods=4, unit="ns"))
    result = methodcaller(method, **method_args)(ser.resample("2D"))

    exp_dti = pd.DatetimeIndex(["2017-01-01", "2017-01-03"], dtype="M8[ns]", freq="2D")
    expected = Series([0.0, unit], index=exp_dti)
    tm.assert_series_equal(result, expected)

