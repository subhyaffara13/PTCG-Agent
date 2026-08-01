
def HolidayCalendarFactory(name: str, base, other, base_class=AbstractHolidayCalendar):
    rules = AbstractHolidayCalendar.merge_class(base, other)
    calendar_class = type(name, (base_class,), {"rules": rules, "name": name})
    return calendar_class

