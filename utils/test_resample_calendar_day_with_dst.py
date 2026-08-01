
def test_resample_calendar_day_with_dst(
    first: str, last: str, freq_in: str, freq_out: str, exp_last: str, unit
):
    # GH 35219
    ts = Series(
        1.0, date_range(first, last, freq=freq_in, tz="Europe/Amsterdam").as_unit(unit)
    )
    result = ts.resample(freq_out).ffill()
    expected = Series(
        1.0,
        date_range(first, exp_last, freq=freq_out, tz="Europe/Amsterdam").as_unit(unit),
    )
    tm.assert_series_equal(result, expected)

