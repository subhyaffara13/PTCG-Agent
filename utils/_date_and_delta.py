from typing import Any

def _date_and_delta(
    value: Any, *, now: dt.datetime | None = None, precise: bool = False
) -> tuple[Any, Any]:
    """Turn a value into a date and a timedelta which represents how long ago it was.

    If that's not possible, return `(None, value)`.
    """
    import datetime as dt

    if not now:
        now = _now()
    if isinstance(value, dt.datetime):
        date = value
        delta = now - value
    elif isinstance(value, dt.timedelta):
        date = now - value
        delta = value
    else:
        try:
            value = value if precise else round(value)
            delta = dt.timedelta(seconds=value)
            date = now - delta
        except (ValueError, TypeError):
            return None, value
    return date, _abs_timedelta(delta)

