
def test_resample_interpolate_regular_sampling_off_grid(
    all_1d_no_arg_interpolation_methods,
):
    pytest.importorskip("scipy")
    # GH#21351
    index = date_range("2000-01-01 00:01:00", periods=5, freq="2h")
    ser = Series(np.arange(5.0), index)

    method = all_1d_no_arg_interpolation_methods
    result = ser.resample("1h").interpolate(method)

    if method == "linear":
        values = np.repeat(np.arange(0.0, 4.0), 2) + np.tile([1 / 3, 2 / 3], 4)
    elif method == "nearest":
        values = np.repeat(np.arange(0.0, 5.0), 2)[1:-1]
    elif method == "zero":
        values = np.repeat(np.arange(0.0, 4.0), 2)
    else:
        values = 0.491667 + np.arange(0.0, 4.0, 0.5)
    values = np.insert(values, 0, np.nan)
    index = date_range("2000-01-01 00:00:00", periods=9, freq="1h")
    expected = Series(values, index=index)
    tm.assert_series_equal(result, expected)

