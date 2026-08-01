
def test_resample_timestamp_to_period(
    simple_date_range_series, freq, expected_kwargs, unit
):
    ts = simple_date_range_series("1/1/1990", "1/1/2000")
    ts.index = ts.index.as_unit(unit)

    result = ts.resample(freq).mean().to_period()
    expected = ts.resample(freq).mean()
    expected.index = period_range(**expected_kwargs)
    tm.assert_series_equal(result, expected)

