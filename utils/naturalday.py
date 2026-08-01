
def naturalday(value: dt.date | dt.datetime, format: str = "%b %d") -> str:
    """Return a natural day.

    For date values that are tomorrow, today or yesterday compared to
    present day return representing string. Otherwise, return a string
    formatted according to `format`.

    """
    import datetime as dt

    try:
        # When value is a tz-aware datetime, compute "today" in that timezone
        # so the comparison uses the correct local date.
        if isinstance(value, dt.datetime) and value.tzinfo is not None:
            today = dt.datetime.now(value.tzinfo).date()
        else:
            today = dt.date.today()
        value = dt.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't date-ish
        return str(value)
    except (OverflowError, ValueError):
        # Date arguments out of range
        return str(value)
    delta = value - today

    if delta.days == 0:
        return _("today")

    if delta.days == 1:
        return _("tomorrow")

    if delta.days == -1:
        return _("yesterday")

    return value.strftime(format)

