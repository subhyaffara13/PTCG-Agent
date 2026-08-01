
def thousands_separator() -> str:
    """Return the thousands separator for a locale, default to comma.

    Returns:
         str: Thousands separator.
    """
    return _THOUSANDS_SEPARATOR.get(getattr(_CURRENT, "locale", None), ",")

