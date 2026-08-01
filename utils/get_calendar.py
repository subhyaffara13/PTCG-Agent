
def get_calendar(name: str) -> AbstractHolidayCalendar:
    """
    Return an instance of a calendar based on its name.

    Parameters
    ----------
    name : str
        Calendar name to return an instance of
    """
    return holiday_calendars[name]()

