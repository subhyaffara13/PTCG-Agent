
def _quotient_and_remainder(
    value: float,
    divisor: float,
    unit: Unit,
    minimum_unit: Unit,
    suppress: Iterable[Unit],
    format: str,
) -> tuple[float, float]:
    """Divide `value` by `divisor`, returning the quotient and remainder.

    If `unit` is `minimum_unit`, the quotient will be the rounding of `value / divisor`
    according to the `format` string and the remainder will be zero. The rationale is
    that if `unit` is the unit of the quotient, we cannot represent the remainder
    because it would require a unit smaller than the `minimum_unit`.

    >>> from humanize.time import _quotient_and_remainder, Unit
    >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.DAYS, [], "%0.2f")
    (1.5, 0)

    If `unit` is in `suppress`, the quotient will be zero and the remainder will be the
    initial value. The idea is that if we cannot use `unit`, we are forced to use a
    lower unit, so we cannot do the division.

    >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [Unit.DAYS], "%0.2f")
    (0, 36)

    In other cases, return the quotient and remainder as `divmod` would do it.

    >>> _quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [], "%0.2f")
    (1, 12)

    """
    if unit == minimum_unit:
        return _rounding_by_fmt(format, value / divisor), 0

    if unit in suppress:
        return 0, value

    # Convert the remainder back to integer is necessary for months. 1 month is 30.5
    # days on average, but if we have 31 days, we want to count is as a whole month,
    # and not as 1 month plus a remainder of 0.5 days.
    q, r = divmod(value, divisor)
    return q, int(r)

