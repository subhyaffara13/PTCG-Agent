
def scientific(value: NumberOrString, precision: int = 2) -> str:
    """Return number in string scientific notation z.wq x 10ⁿ.

    Examples:
        ```pycon
        >>> scientific(float(0.3))
        '3.00 x 10⁻¹'
        >>> scientific(int(500))
        '5.00 x 10²'
        >>> scientific(-1000)
        '-1.00 x 10³'
        >>> scientific(1000, 1)
        '1.0 x 10³'
        >>> scientific(1000, 3)
        '1.000 x 10³'
        >>> scientific("99")
        '9.90 x 10¹'
        >>> scientific("foo")
        'foo'
        >>> scientific(None)
        'None'

        ```

    Args:
        value (int, float, str): Input number.
        precision (int): Number of decimal for first part of the number.

    Returns:
        str: Number in scientific notation z.wq x 10ⁿ.
    """
    import math

    try:
        value = float(value)
        if not math.isfinite(value):
            return _format_not_finite(value)
    except (ValueError, TypeError):
        return str(value)
    fmt = f"{{:.{int(precision)}e}}"
    n = fmt.format(value)
    part1, part2 = n.split("e")
    # Normalise exponent: int() strips the "+" sign and leading zeros,
    # while preserving "-" and a single "0" for 10⁰.
    return part1 + " x 10" + str(int(part2)).translate(_SUPERSCRIPT_TRANS)

