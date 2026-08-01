
def test_holidays_with_timezone_specified_but_no_occurrences():
    # GH 54580
    # _apply_rule() in holiday.py was silently dropping timezones if you passed it
    # an empty list of holiday dates that had timezone information
    start_date = Timestamp("2018-01-01", tz="America/Chicago")
    end_date = Timestamp("2018-01-11", tz="America/Chicago")
    test_case = USFederalHolidayCalendar().holidays(
        start_date, end_date, return_name=True
    )
    expected_results = Series("New Year's Day", index=[start_date])

    tm.assert_equal(test_case, expected_results)

