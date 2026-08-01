
def test_rule_from_name():
    us_fed_cal = get_calendar("USFederalHolidayCalendar")
    assert us_fed_cal.rule_from_name("Thanksgiving Day") == USThanksgivingDay

