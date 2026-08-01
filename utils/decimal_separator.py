
def decimal_separator() -> str:
    """Return the decimal separator for a locale, default to dot.

    Returns:
         str: Decimal separator.
    """
    return _DECIMAL_SEPARATOR.get(getattr(_CURRENT, "locale", None), ".")

