
def test_dt_tz_localize_none(request):
    _require_timezone_database(request)

    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns", tz="US/Pacific")),
    )
    result = ser.dt.tz_localize(None)
    expected = pd.Series(
        [ser[0].tz_localize(None), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    tm.assert_series_equal(result, expected)

