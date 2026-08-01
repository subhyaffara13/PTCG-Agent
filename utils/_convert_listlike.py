
def _convert_listlike(
    arg,
    unit: UnitChoices | None = None,
    errors: DateTimeErrorChoices = "raise",
    name: Hashable | None = None,
):
    """Convert a list of objects to a timedelta index object."""
    arg_dtype = getattr(arg, "dtype", None)
    if isinstance(arg, (list, tuple)) or arg_dtype is None:
        arg = np.array(arg, dtype=object)
    elif isinstance(arg_dtype, ArrowDtype) and arg_dtype.kind == "m":
        return arg

    td64arr = sequence_to_td64ns(arg, unit=unit, errors=errors, copy=False)[0]

    from pandas import TimedeltaIndex

    copy = td64arr is arg or np.may_share_memory(arg, td64arr)
    value = TimedeltaIndex(td64arr, name=name, copy=copy)
    return value

