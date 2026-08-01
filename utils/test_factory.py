
def test_factory():
    class_1 = HolidayCalendarFactory(
        "MemorialDay", AbstractHolidayCalendar, USMemorialDay
    )
    class_2 = HolidayCalendarFactory(
        "Thanksgiving", AbstractHolidayCalendar, USThanksgivingDay
    )
    class_3 = HolidayCalendarFactory("Combined", class_1, class_2)

    assert len(class_1.rules) == 1
    assert len(class_2.rules) == 1
    assert len(class_3.rules) == 2

