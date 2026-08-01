
def test_cache_keys_are_distinct_for_pytz_vs_dateutil():
    pytz = pytest.importorskip("pytz")
    for tz_name in pytz.common_timezones:
        tz_p = timezones.maybe_get_tz(tz_name)
        tz_d = timezones.maybe_get_tz("dateutil/" + tz_name)

    if tz_d is None:
        pytest.skip(tz_name + ": dateutil does not know about this one")

    if not (tz_name == "UTC" and is_platform_windows()):
        # they both end up as tzwin("UTC") on windows
        assert timezones._p_tz_cache_key(tz_p) != timezones._p_tz_cache_key(tz_d)

