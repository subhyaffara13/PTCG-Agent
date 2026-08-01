
def attempt_conversion(value: T) -> T:
    """
    >>> is_static(attempt_conversion("hello"))
    True
    >>> is_static(object())
    False
    """
    return _CONVERSIONS.get(type(value), noop)(value)  # type: ignore[call-overload]

