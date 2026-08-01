
def ensure_str(s, encoding='utf-8', errors='strict'):
    """Coerce *s* to `str`.

    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`

    For Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`
    """
    # Optimization: Fast return for the common case.
    if type(s) is str:
        return s
    if PY2 and isinstance(s, text_type):
        return s.encode(encoding, errors)
    elif PY3 and isinstance(s, binary_type):
        return s.decode(encoding, errors)
    elif not isinstance(s, (text_type, binary_type)):
        raise TypeError("not expecting type '%s'" % type(s))
    return s


def ensure_str(value: Optional[Union[str, bytes]]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8")  # or whatever encoding is right
    return value


def ensure_str(value: bytes | Any) -> str:
    """
    Ensure that bytes and non-strings get converted into ``str`` objects.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    elif not isinstance(value, str):
        value = str(value)
    return value


def ensure_str(s):
    if s is None:
        return None
    elif isinstance(s, text_type):
        return s
    else:
        return s.decode("ascii", "strict")

