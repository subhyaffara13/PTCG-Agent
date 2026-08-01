
def test_holidays_within_dates(holiday, start, expected):
    # see gh-11477
    #
    # Fix holiday behavior where holiday.dates returned dates outside
    # start/end date, or observed rules could not be applied because the
    # holiday was not in the original date range (e.g., 7/4/2015 -> 7/3/2015).
    if isinstance(holiday, str):
        calendar = get_calendar("USFederalHolidayCalendar")
        holiday = calendar.rule_from_name(holiday)

    assert list(holiday.dates(start, start)) == expected

    # Verify that timezone info is preserved.
    assert list(
        holiday.dates(
            Timestamp(start, tz=timezone.utc), Timestamp(start, tz=timezone.utc)
        )
    ) == [dt.replace(tzinfo=timezone.utc) for dt in expected]

