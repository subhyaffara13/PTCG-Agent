
def test_dt_strftime(request):
    _require_timezone_database(request)

    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    result = ser.dt.strftime("%Y-%m-%dT%H:%M:%S")
    expected = pd.Series(
        ["2023-01-02T03:00:00.000000000", None], dtype=ArrowDtype(pa.string())
    )
    tm.assert_series_equal(result, expected)

