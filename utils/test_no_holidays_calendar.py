
def test_no_holidays_calendar():
    # Test for issue #31415

    class NoHolidaysCalendar(AbstractHolidayCalendar):
        pass

    cal = NoHolidaysCalendar()
    holidays = cal.holidays(Timestamp("01-Jan-2020"), Timestamp("01-Jan-2021"))
    empty_index = DatetimeIndex([])  # Type is DatetimeIndex since return_name=False
    tm.assert_index_equal(holidays, empty_index)

