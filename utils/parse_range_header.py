
def parse_range_header(
    value: str | None, make_inclusive: bool = True
) -> ds.Range | None:
    """Parses a range header into a :class:`~werkzeug.datastructures.Range`
    object.  If the header is missing or malformed `None` is returned.
    `ranges` is a list of ``(start, stop)`` tuples where the ranges are
    non-inclusive.

    .. versionadded:: 0.7
    """
    if not value or "=" not in value:
        return None

    ranges = []
    last_end = 0
    units, rng = value.split("=", 1)
    units = units.strip().lower()

    for item in rng.split(","):
        item = item.strip()
        if "-" not in item:
            return None
        if item.startswith("-"):
            if last_end < 0:
                return None
            try:
                begin = _plain_int(item)
            except ValueError:
                return None
            end = None
            last_end = -1
        elif "-" in item:
            begin_str, end_str = item.split("-", 1)
            begin_str = begin_str.strip()
            end_str = end_str.strip()

            try:
                begin = _plain_int(begin_str)
            except ValueError:
                return None

            if begin < last_end or last_end < 0:
                return None
            if end_str:
                try:
                    end = _plain_int(end_str) + 1
                except ValueError:
                    return None

                if begin >= end:
                    return None
            else:
                end = None
            last_end = end if end is not None else -1
        ranges.append((begin, end))

    return ds.Range(units, ranges)

