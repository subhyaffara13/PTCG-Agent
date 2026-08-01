
def test_get_calendar():
    class TestCalendar(AbstractHolidayCalendar):
        rules = []

    calendar = get_calendar("TestCalendar")
    assert TestCalendar == type(calendar)

