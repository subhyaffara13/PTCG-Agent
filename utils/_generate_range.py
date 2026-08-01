
def _generate_range(
    start: Timestamp | None,
    end: Timestamp | None,
    periods: int | None,
    offset: BaseOffset,
    *,
    unit: TimeUnit,
) -> Generator[Timestamp]:
    """
    Generates a sequence of dates corresponding to the specified time
    offset. Similar to dateutil.rrule except uses pandas DateOffset
    objects to represent time increments.

    Parameters
    ----------
    start : Timestamp or None
    end : Timestamp or None
    periods : int or None
    offset : DateOffset
    unit : str

    Notes
    -----
    * This method is faster for generating weekdays than dateutil.rrule
    * At least two of (start, end, periods) must be specified.
    * If both start and end are specified, the returned dates will
    satisfy start <= date <= end.

    Returns
    -------
    dates : generator object
    """
    offset = to_offset(offset)

    # Argument 1 to "Timestamp" has incompatible type "Optional[Timestamp]";
    # expected "Union[integer[Any], float, str, date, datetime64]"
    start = Timestamp(start)  # type: ignore[arg-type]
    if start is not NaT:
        start = start.as_unit(unit)
    else:
        start = None

    # Argument 1 to "Timestamp" has incompatible type "Optional[Timestamp]";
    # expected "Union[integer[Any], float, str, date, datetime64]"
    end = Timestamp(end)  # type: ignore[arg-type]
    if end is not NaT:
        end = end.as_unit(unit)
    else:
        end = None

    # GH #64834 FIX for bdate_range regression
    if end is not None and periods is not None and not offset.is_on_offset(end):
        if offset.n >= 0:
            end = offset.rollback(end)  # type: ignore[assignment]
        else:
            end = offset.rollforward(end)  # type: ignore[assignment]

    if start and not offset.is_on_offset(start):
        # Incompatible types in assignment (expression has type "datetime",
        # variable has type "Optional[Timestamp]")

        # GH #56147 account for negative direction and range bounds
        if offset.n >= 0:
            start = offset.rollforward(start)  # type: ignore[assignment]
        else:
            start = offset.rollback(start)  # type: ignore[assignment]

    # Unsupported operand types for < ("Timestamp" and "None")
    if periods is None and end < start and offset.n >= 0:  # type: ignore[operator]
        end = None
        periods = 0

    if end is None:
        # error: No overload variant of "__radd__" of "BaseOffset" matches
        # argument type "None"
        end = start + (periods - 1) * offset  # type: ignore[operator]

    if start is None:
        # error: No overload variant of "__radd__" of "BaseOffset" matches
        # argument type "None"
        start = end - (periods - 1) * offset  # type: ignore[operator]

    start = cast(Timestamp, start)
    end = cast(Timestamp, end)

    cur = start
    if offset.n >= 0:
        while cur <= end:
            yield cur

            if cur == end:
                # GH#24252 avoid overflows by not performing the addition
                # in offset.apply unless we have to
                break

            # faster than cur + offset
            next_date = offset._apply(cur)
            next_date = next_date.as_unit(unit)
            if next_date <= cur:
                raise ValueError(f"Offset {offset} did not increment date")
            cur = next_date
    else:
        while cur >= end:
            yield cur

            if cur == end:
                # GH#24252 avoid overflows by not performing the addition
                # in offset.apply unless we have to
                break

            # faster than cur + offset
            next_date = offset._apply(cur)
            next_date = next_date.as_unit(unit)
            if next_date >= cur:
                raise ValueError(f"Offset {offset} did not decrement date")
            cur = next_date

