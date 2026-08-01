
def _date_from_string(s: str) -> datetime:
    order = ("year", "month", "day", "hour", "minute", "second")
    m = _date_parser.match(s)
    if m is None:
        raise ValueError(f"Expected ISO 8601 date string, but got '{s:r}'.")
    gd = m.groupdict()
    lst = []
    for key in order:
        val = gd[key]
        if val is None:
            break
        lst.append(int(val))
    # NOTE: mypy doesn't know that lst is 6 elements long.
    return datetime(*lst)  # type:ignore

