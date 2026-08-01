
def test_holiday_dates(holiday, start_date, end_date, expected):
    assert list(holiday.dates(start_date, end_date)) == expected

    # Verify that timezone info is preserved.
    assert list(
        holiday.dates(
            Timestamp(start_date, tz=timezone.utc), Timestamp(end_date, tz=timezone.utc)
        )
    ) == [dt.replace(tzinfo=timezone.utc) for dt in expected]

