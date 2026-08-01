
def test_tz_convert_single_matches_tz_convert(tz_aware_fixture, freq):
    tz = tz_aware_fixture
    tz_didx = date_range("2018-01-01", "2020-01-01", freq=freq, tz=tz, unit="ns")
    naive_didx = date_range("2018-01-01", "2020-01-01", freq=freq, unit="ns")

    _compare_utc_to_local(tz_didx)
    _compare_local_to_utc(tz_didx, naive_didx)

