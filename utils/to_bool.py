
def to_bool(val):
    """
    Convert "boolean" strings (for example, from environment variables) to real
    booleans.

    Values mapping to `True`:

    - ``True``
    - ``"true"`` / ``"t"``
    - ``"yes"`` / ``"y"``
    - ``"on"``
    - ``"1"``
    - ``1``

    Values mapping to `False`:

    - ``False``
    - ``"false"`` / ``"f"``
    - ``"no"`` / ``"n"``
    - ``"off"``
    - ``"0"``
    - ``0``

    Raises:
        ValueError: For any other value.

    .. versionadded:: 21.3.0
    """
    if isinstance(val, str):
        val = val.lower()

    if val in (True, "true", "t", "yes", "y", "on", "1", 1):
        return True
    if val in (False, "false", "f", "no", "n", "off", "0", 0):
        return False

    msg = f"Cannot convert value to bool: {val!r}"
    raise ValueError(msg)


def to_bool(value):
    if value is None or value == "":
        return None
    if isinstance(value, str) and value.upper() in FALSE_STRINGS:
        return False
    return bool(value)


def to_bool(value) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, str) and value.upper() in FALSE_STRINGS:
        return False
    return bool(value)

