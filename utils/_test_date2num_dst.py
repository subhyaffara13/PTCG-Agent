
def _test_date2num_dst(date_range, tz_convert):
    # Timezones

    BRUSSELS = dateutil.tz.gettz('Europe/Brussels')
    UTC = mdates.UTC

    # Create a list of timezone-aware datetime objects in UTC
    # Interval is 0b0.0000011 days, to prevent float rounding issues
    dtstart = datetime.datetime(2014, 3, 30, 0, 0, tzinfo=UTC)
    interval = datetime.timedelta(minutes=33, seconds=45)
    interval_days = interval.seconds / 86400
    N = 8

    dt_utc = date_range(start=dtstart, freq=interval, periods=N)
    dt_bxl = tz_convert(dt_utc, BRUSSELS)
    t0 = 735322.0 + mdates.date2num(np.datetime64('0000-12-31'))
    expected_ordinalf = [t0 + (i * interval_days) for i in range(N)]
    actual_ordinalf = list(mdates.date2num(dt_bxl))

    assert actual_ordinalf == expected_ordinalf

