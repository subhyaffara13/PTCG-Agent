
def _to_int(s: str) -> Union[int, str]:
    try:
        return int(s)
    except ValueError:
        return s


def _to_int(x: bytes | str) -> int:
    # Some AFM files have floats where we are expecting ints -- there is
    # probably a better way to handle this (support floats, round rather than
    # truncate).  But I don't know what the best approach is now and this
    # change to _to_int should at least prevent Matplotlib from crashing on
    # these.  JDH (2009-11-06)
    return int(float(x))


def _to_int(s: str) -> int | str:
    try:
        return int(s)
    except ValueError:
        return s


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_int(x: int | Array | None) -> int | None:
  """Converts a value to an integer, or returns None if the value is None."""
  if x is None:
    return None
  return int(x)

