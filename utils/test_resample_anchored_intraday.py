
def test_resample_anchored_intraday(unit):
    # #1471, #1458

    rng = date_range("1/1/2012", "4/1/2012", freq="100min").as_unit(unit)
    df = DataFrame(rng.month, index=rng)

    result = df.resample("ME").mean()
    expected = df.resample("ME").mean().to_period()
    expected = expected.to_timestamp(how="end")
    expected.index += Timedelta(1, unit="us") - Timedelta(1, unit="D")
    expected.index = expected.index.as_unit(unit)._with_freq("infer")
    assert expected.index.freq == "ME"
    tm.assert_frame_equal(result, expected)

    result = df.resample("ME", closed="left").mean()
    exp = df.shift(1, freq="D").resample("ME").mean().to_period()
    exp = exp.to_timestamp(how="end")

    exp.index = exp.index + Timedelta(1, unit="us") - Timedelta(1, unit="D")
    exp.index = exp.index.as_unit(unit)._with_freq("infer")
    assert exp.index.freq == "ME"
    tm.assert_frame_equal(result, exp)

