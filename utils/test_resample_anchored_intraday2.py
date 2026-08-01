
def test_resample_anchored_intraday2(unit):
    rng = date_range("1/1/2012", "4/1/2012", freq="100min").as_unit(unit)
    df = DataFrame(rng.month, index=rng)

    result = df.resample("QE").mean()
    expected = df.resample("QE").mean().to_period()
    expected = expected.to_timestamp(how="end")
    expected.index += Timedelta(1, unit="us") - Timedelta(1, unit="D")
    expected.index._data.freq = "QE"
    expected.index._freq = lib.no_default
    expected.index = expected.index.as_unit(unit)
    tm.assert_frame_equal(result, expected)

    result = df.resample("QE", closed="left").mean()
    expected = df.shift(1, freq="D").resample("QE").mean()
    expected = expected.to_period()
    expected = expected.to_timestamp(how="end")
    expected.index += Timedelta(1, unit="us") - Timedelta(1, unit="D")
    expected.index._data.freq = "QE"
    expected.index._freq = lib.no_default
    expected.index = expected.index.as_unit(unit)
    tm.assert_frame_equal(result, expected)

