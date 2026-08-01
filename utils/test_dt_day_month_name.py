
def test_dt_day_month_name(method, exp, request):
    # GH 52388
    _require_timezone_database(request)

    ser = pd.Series([datetime(2023, 1, 1), None], dtype=ArrowDtype(pa.timestamp("ms")))
    result = getattr(ser.dt, method)()
    expected = pd.Series([exp, None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

