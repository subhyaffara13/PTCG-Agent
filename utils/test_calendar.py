
def test_calendar(transform):
    start_date = datetime(2012, 1, 1)
    end_date = datetime(2012, 12, 31)

    calendar = USFederalHolidayCalendar()
    holidays = calendar.holidays(transform(start_date), transform(end_date))

    expected = [
        datetime(2012, 1, 2),
        datetime(2012, 1, 16),
        datetime(2012, 2, 20),
        datetime(2012, 5, 28),
        datetime(2012, 7, 4),
        datetime(2012, 9, 3),
        datetime(2012, 10, 8),
        datetime(2012, 11, 12),
        datetime(2012, 11, 22),
        datetime(2012, 12, 25),
    ]

    assert list(holidays.to_pydatetime()) == expected

