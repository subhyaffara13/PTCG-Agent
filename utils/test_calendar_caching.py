
def test_calendar_caching():
    # see gh-9552.

    class TestCalendar(AbstractHolidayCalendar):
        def __init__(self, name=None, rules=None) -> None:
            super().__init__(name=name, rules=rules)

    jan1 = TestCalendar(rules=[Holiday("jan1", year=2015, month=1, day=1)])
    jan2 = TestCalendar(rules=[Holiday("jan2", year=2015, month=1, day=2)])

    # Getting holidays for Jan 1 should not alter results for Jan 2.
    expected = DatetimeIndex(["01-Jan-2015"]).as_unit("us")
    tm.assert_index_equal(jan1.holidays(), expected)

    expected2 = DatetimeIndex(["02-Jan-2015"]).as_unit("us")
    tm.assert_index_equal(jan2.holidays(), expected2)

