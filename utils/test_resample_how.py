
def test_resample_how(downsample_method, unit):
    if downsample_method == "ohlc":
        pytest.skip("covered by test_resample_how_ohlc")
    index = date_range("1/1/2000 00:00:00", "1/1/2000 00:13:00", freq="Min")
    s = Series(range(len(index)), index=index)
    s.index.name = "index"
    s.index = s.index.as_unit(unit)
    grouplist = np.ones_like(s)
    grouplist[0] = 0
    grouplist[1:6] = 1
    grouplist[6:11] = 2
    grouplist[11:] = 3
    expected = s.groupby(grouplist).agg(downsample_method)
    expected.index = date_range(
        "1/1/2000", periods=4, freq="5min", name="index"
    ).as_unit(unit)

    result = getattr(
        s.resample("5min", closed="right", label="right"), downsample_method
    )()
    tm.assert_series_equal(result, expected)

