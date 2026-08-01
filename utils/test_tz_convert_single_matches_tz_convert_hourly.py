
def test_tz_convert_single_matches_tz_convert_hourly(tz_aware_fixture):
    tz = tz_aware_fixture
    tz_didx = date_range("2014-03-01", "2014-04-01", freq="h", tz=tz, unit="ns")
    naive_didx = date_range("2014-03-01", "2014-04-01", freq="h", unit="ns")

    _compare_utc_to_local(tz_didx)
    _compare_local_to_utc(tz_didx, naive_didx)

