
def test_calendar_observance_dates():
    # see gh-11477
    us_fed_cal = get_calendar("USFederalHolidayCalendar")
    holidays0 = us_fed_cal.holidays(
        datetime(2015, 7, 3), datetime(2015, 7, 3)
    )  # <-- same start and end dates
    holidays1 = us_fed_cal.holidays(
        datetime(2015, 7, 3), datetime(2015, 7, 6)
    )  # <-- different start and end dates
    holidays2 = us_fed_cal.holidays(
        datetime(2015, 7, 3), datetime(2015, 7, 3)
    )  # <-- same start and end dates

    # These should all produce the same result.
    #
    # In addition, calling with different start and end
    # dates should not alter the output if we call the
    # function again with the same start and end date.
    tm.assert_index_equal(holidays0, holidays1)
    tm.assert_index_equal(holidays0, holidays2)

