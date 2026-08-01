
def test_dt_tz_localize_nonexistent(nonexistent, exp_date, request):
    _require_timezone_database(request)

    ser = pd.Series(
        [datetime(year=2023, month=3, day=12, hour=2, minute=30), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    result = ser.dt.tz_localize("US/Pacific", nonexistent=nonexistent)
    exp_data = pa.array([exp_date, None], type=pa.timestamp("ns"))
    exp_data = pa.compute.assume_timezone(exp_data, "US/Pacific")
    expected = pd.Series(ArrowExtensionArray(exp_data))
    tm.assert_series_equal(result, expected)

