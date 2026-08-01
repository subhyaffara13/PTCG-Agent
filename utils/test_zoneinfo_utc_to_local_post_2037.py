
def test_zoneinfo_utc_to_local_post_2037():
    # GH#64363 - verify that ZoneInfo DST transitions after 2037
    # (generated from POSIX TZ string rules) produce correct local times.
    tz = zoneinfo.ZoneInfo("US/Pacific")
    utc_times = date_range("2040-07-01", periods=24, freq="h", tz="UTC")
    local = utc_times.tz_convert(tz)

    expected_hours = np.array(
        [
            datetime(2040, 7, 1, hour, tzinfo=timezone.utc).astimezone(tz).hour
            for hour in range(24)
        ],
        dtype=np.int32,
    )
    tm.assert_numpy_array_equal(local.hour.to_numpy(), expected_hours)

