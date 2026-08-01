
def naturaldate(value: dt.date | dt.datetime) -> str:
    """Like `naturalday`, but append a year for dates more than ~five months away."""
    import datetime as dt

    original_value = value
    try:
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
    delta = _abs_timedelta(value - today)
    if delta.days >= 5 * 365 / 12:
        return naturalday(original_value, "%b %d %Y")
    return naturalday(original_value)

