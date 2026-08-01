
def naturaldelta(
    value: dt.timedelta | float,
    months: bool = True,
    minimum_unit: str = "seconds",
) -> str:
    """Return a natural representation of a timedelta or number of seconds.

    This is similar to `naturaltime`, but does not add tense to the result.

    The timedelta will be rounded to the nearest unit that makes sense.

    Args:
        value (datetime.timedelta, int or float): A timedelta or a number of seconds.
        months (bool): If `True`, then a number of months (based on 30.5 days) will be
            used for fuzziness between years.
        minimum_unit (str): The lowest unit that can be used.

    Returns:
        str (str or `value`): A natural representation of the amount of time
            elapsed unless `value` is not datetime.timedelta or cannot be
            converted to int (cannot be float due to 'inf' or 'nan').
            In that case, a `value` is returned unchanged.

    Raises:
        OverflowError: If `value` is too large to convert to datetime.timedelta.

    Examples:
        Compare two timestamps in a custom local timezone::

        ```pycon
        >>> import datetime as dt
        >>> from dateutil.tz import gettz

        >>> berlin = gettz("Europe/Berlin")
        >>> now = dt.datetime.now(tz=berlin)
        >>> later = now + dt.timedelta(minutes=30)

        >>> assert naturaldelta(later - now) == "30 minutes"
        True
        ```

    """
    import datetime as dt

    tmp = Unit[minimum_unit.upper()]
    if tmp not in (Unit.SECONDS, Unit.MILLISECONDS, Unit.MICROSECONDS):
        msg = f"Minimum unit '{minimum_unit}' not supported"
        raise ValueError(msg)
    min_unit = tmp

    if isinstance(value, dt.timedelta):
        delta = value
    else:
        try:
            int(value)  # Explicitly don't support string such as "NaN" or "inf"
            value = float(value)
            delta = dt.timedelta(seconds=value)
        except (ValueError, TypeError):
            return str(value)

    use_months = months

    delta = abs(delta)
    years = delta.days // 365
    days = delta.days % 365
    num_months = round(days / 30.5)

    if years == 0 and days < 1:
        if delta.seconds == 0:
            if min_unit == Unit.MICROSECONDS and delta.microseconds < 1000:
                return (
                    _ngettext("%d microsecond", "%d microseconds", delta.microseconds)
                    % delta.microseconds
                )

            if min_unit == Unit.MILLISECONDS or (
                min_unit == Unit.MICROSECONDS and 1000 <= delta.microseconds < 1_000_000
            ):
                milliseconds = delta.microseconds / 1000
                return (
                    _ngettext("%d millisecond", "%d milliseconds", int(milliseconds))
                    % milliseconds
                )
            return _("a moment")

        if delta.seconds == 1:
            return _("a second")

        if delta.seconds < 60:
            return _ngettext("%d second", "%d seconds", delta.seconds) % delta.seconds

        if 60 <= delta.seconds < 3600:
            minutes = round(delta.seconds / 60)
            if minutes == 1:
                return _("a minute")

            if minutes == 60:
                return _("an hour")

            return _ngettext("%d minute", "%d minutes", minutes) % minutes

        if 3600 <= delta.seconds:
            hours = round(delta.seconds / 3600)
            if hours == 1:
                return _("an hour")

            if hours == 24:
                return _("a day")

            return _ngettext("%d hour", "%d hours", hours) % hours

    elif years == 0:
        if days == 1:
            return _("a day")

        if not use_months:
            return _ngettext("%d day", "%d days", days) % days

        if num_months == 0:
            return _ngettext("%d day", "%d days", days) % days

        if num_months == 1:
            return _("a month")

        if num_months == 12:
            return _("a year")

        return _ngettext("%d month", "%d months", num_months) % num_months

    elif years == 1:
        if num_months == 0 and days == 0:
            return _("a year")

        if num_months == 0:
            return _ngettext("1 year, %d day", "1 year, %d days", days) % days

        if use_months:
            if num_months == 1:
                return _("1 year, 1 month")

            if num_months == 12:
                years += 1
                return _ngettext("%d year", "%d years", years) % years

            return (
                _ngettext("1 year, %d month", "1 year, %d months", num_months)
                % num_months
            )

        return _ngettext("1 year, %d day", "1 year, %d days", days) % days

    return _ngettext("%d year", "%d years", years).replace("%d", "%s") % intcomma(years)

