
def precisedelta(
    value: dt.timedelta | float | None,
    minimum_unit: str = "seconds",
    suppress: Iterable[str] = (),
    format: str = "%0.2f",
) -> str:
    """Return a precise representation of a timedelta or number of seconds.

    ```pycon
    >>> import datetime as dt
    >>> from humanize.time import precisedelta

    >>> delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
    >>> precisedelta(delta)
    '2 days, 1 hour and 33.12 seconds'

    ```

    A custom `format` can be specified to control how the fractional part
    is represented:

    ```pycon
    >>> precisedelta(delta, format="%0.4f")
    '2 days, 1 hour and 33.1230 seconds'

    ```

    Instead, the `minimum_unit` can be changed to have a better resolution;
    the function will still readjust the unit to use the greatest of the
    units that does not lose precision.

    For example setting microseconds but still representing the date with milliseconds:

    ```pycon
    >>> precisedelta(delta, minimum_unit="microseconds")
    '2 days, 1 hour, 33 seconds and 123 milliseconds'

    ```

    If desired, some units can be suppressed: you will not see them represented and the
    time of the other units will be adjusted to keep representing the same timedelta:

    ```pycon
    >>> precisedelta(delta, suppress=['days'])
    '49 hours and 33.12 seconds'

    ```

    Note that microseconds precision is lost if the seconds and all
    the units below are suppressed:

    ```pycon
    >>> delta = dt.timedelta(seconds=90, microseconds=100)
    >>> precisedelta(delta, suppress=['seconds', 'milliseconds', 'microseconds'])
    '1.50 minutes'

    ```

    If the delta is too small to be represented with the minimum unit,
    a value of zero will be returned:

    ```pycon
    >>> delta = dt.timedelta(seconds=1)
    >>> precisedelta(delta, minimum_unit="minutes")
    '0.02 minutes'

    >>> delta = dt.timedelta(seconds=0.1)
    >>> precisedelta(delta, minimum_unit="minutes")
    '0 minutes'

    ```
    """
    date, delta = _date_and_delta(value, precise=True)
    if date is None:
        return str(value)

    suppress_set = {Unit[s.upper()] for s in suppress}

    # Find a suitable minimum unit (it can be greater than the one that the
    # user gave us, if that one is suppressed).
    min_unit = Unit[minimum_unit.upper()]
    min_unit = _suitable_minimum_unit(min_unit, suppress_set)
    del minimum_unit

    # Expand the suppressed units list/set to include all the units
    # that are below the minimum unit
    suppress_set = _suppress_lower_units(min_unit, suppress_set)

    # handy aliases
    days = delta.days
    secs = delta.seconds
    usecs = delta.microseconds

    MILLISECONDS = Unit.MILLISECONDS
    SECONDS = Unit.SECONDS
    MINUTES = Unit.MINUTES
    HOURS = Unit.HOURS
    DAYS = Unit.DAYS
    MONTHS = Unit.MONTHS
    YEARS = Unit.YEARS

    # Given DAYS compute YEARS and the remainder of DAYS as follows:
    #   if YEARS is the minimum unit, we cannot use DAYS so
    #   we will use a float for YEARS and 0 for DAYS:
    #       years, days = years/days, 0
    #
    #   if YEARS is suppressed, use DAYS:
    #       years, days = 0, days
    #
    #   otherwise:
    #       years, days = divmod(years, days)
    #
    # The same applies for months, hours, minutes and milliseconds below
    years, days = _quotient_and_remainder(
        days, 365, YEARS, min_unit, suppress_set, format
    )
    months, days = _quotient_and_remainder(
        days, 30.5, MONTHS, min_unit, suppress_set, format
    )

    secs = days * 24 * 3600 + secs
    days, secs = _quotient_and_remainder(
        secs, 24 * 3600, DAYS, min_unit, suppress_set, format
    )

    hours, secs = _quotient_and_remainder(
        secs, 3600, HOURS, min_unit, suppress_set, format
    )
    minutes, secs = _quotient_and_remainder(
        secs, 60, MINUTES, min_unit, suppress_set, format
    )

    usecs = secs * 1e6 + usecs
    secs, usecs = _quotient_and_remainder(
        usecs, 1e6, SECONDS, min_unit, suppress_set, format
    )

    msecs, usecs = _quotient_and_remainder(
        usecs, 1000, MILLISECONDS, min_unit, suppress_set, format
    )

    # Due to rounding, it could be that a unit is high enough to be promoted to a higher
    # unit. Example: 59.9 minutes was rounded to 60 minutes, and thus it should become 0
    # minutes and one hour more.
    if msecs >= 1_000 and SECONDS not in suppress_set:
        msecs -= 1_000
        secs += 1
    if secs >= 60 and MINUTES not in suppress_set:
        secs -= 60
        minutes += 1
    if minutes >= 60 and HOURS not in suppress_set:
        minutes -= 60
        hours += 1
    if hours >= 24 and DAYS not in suppress_set:
        hours -= 24
        days += 1
    # When adjusting we should not deal anymore with fractional days as all rounding has
    # been already made. We promote 31 days to an extra month.
    if days >= 31 and MONTHS not in suppress_set:
        days -= 31
        months += 1
    if months >= 12 and YEARS not in suppress_set:
        months -= 12
        years += 1

    fmts = [
        ("%d year", "%d years", years),
        ("%d month", "%d months", months),
        ("%d day", "%d days", days),
        ("%d hour", "%d hours", hours),
        ("%d minute", "%d minutes", minutes),
        ("%d second", "%d seconds", secs),
        ("%d millisecond", "%d milliseconds", msecs),
        ("%d microsecond", "%d microseconds", usecs),
    ]

    import math

    texts: list[str] = []
    for unit, fmt in zip(reversed(Unit), fmts):
        singular_txt, plural_txt, fmt_value = fmt
        if fmt_value > 0 or (not texts and unit == min_unit):
            _fmt_value = 2 if 1 < fmt_value < 2 else int(fmt_value)
            fmt_txt = _ngettext(singular_txt, plural_txt, _fmt_value)
            if unit == min_unit and math.modf(fmt_value)[0] > 0:
                fmt_txt = fmt_txt.replace("%d", format)
            elif unit == YEARS:
                if math.modf(fmt_value)[0] == 0:
                    fmt_value = int(fmt_value)
                fmt_txt = fmt_txt.replace("%d", "%s")
                texts.append(fmt_txt % intcomma(fmt_value))
                continue

            texts.append(fmt_txt % fmt_value)

        if unit == min_unit:
            break

    if len(texts) == 1:
        return texts[0]

    head = ", ".join(texts[:-1])
    tail = texts[-1]

    return _("%s and %s") % (head, tail)

