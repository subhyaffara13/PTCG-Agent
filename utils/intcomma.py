
def intcomma(value: NumberOrString, ndigits: int | None = None) -> str:
    """Converts an integer to a string containing commas every three digits.

    For example, 3000 becomes "3,000" and 45000 becomes "45,000". To maintain some
    compatibility with Django's `intcomma`, this function also accepts floats.

    Examples:
        ```pycon
        >>> intcomma(100)
        '100'
        >>> intcomma("1000")
        '1,000'
        >>> intcomma(1_000_000)
        '1,000,000'
        >>> intcomma(1_234_567.25)
        '1,234,567.25'
        >>> intcomma(1234.5454545, 2)
        '1,234.55'
        >>> intcomma(14308.40, 1)
        '14,308.4'
        >>> intcomma("14308.40", 1)
        '14,308.4'
        >>> intcomma(None)
        'None'

        ```

    Args:
        value (int, float, str): Integer or float to convert.
        ndigits (int, None): Digits of precision for rounding after the decimal point.

    Returns:
        str: String containing commas every three digits.
    """
    import math

    thousands_sep = thousands_separator()
    decimal_sep = decimal_separator()
    try:
        if isinstance(value, str):
            value = value.replace(thousands_sep, "").replace(decimal_sep, ".")
            if not math.isfinite(float(value)):
                return _format_not_finite(float(value))
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        else:
            if not math.isfinite(float(value)):
                return _format_not_finite(float(value))
            float(value)
    except (TypeError, ValueError):
        return str(value)

    if ndigits is not None:
        result = f"{value:,.{ndigits}f}"
    else:
        result = f"{value:,}"
    if thousands_sep != "," or decimal_sep != ".":
        result = result.translate(str.maketrans(",.", thousands_sep + decimal_sep))
    return result

