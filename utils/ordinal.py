
def ordinal(value: NumberOrString, gender: str = "male") -> str:
    """Converts an integer to its ordinal as a string.

    For example, 1 is "1st", 2 is "2nd", 3 is "3rd", etc. Works for any integer or
    anything `int()` will turn into an integer. Anything else will return the output
    of str(value).

    Examples:
        ```pycon
        >>> ordinal(1)
        '1st'
        >>> ordinal(1002)
        '1002nd'
        >>> ordinal(103)
        '103rd'
        >>> ordinal(4)
        '4th'
        >>> ordinal(12)
        '12th'
        >>> ordinal(101)
        '101st'
        >>> ordinal(111)
        '111th'
        >>> ordinal("something else")
        'something else'
        >>> ordinal([1, 2, 3]) == "[1, 2, 3]"
        True

        ```

    Args:
        value (int, str, float): Integer to convert.
        gender (str): Gender for translations. Accepts either "male" or "female".

    Returns:
        str: Ordinal string.
    """
    import math

    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    gender = "male" if gender == "male" else "female"
    digit = 0 if value % 100 in (11, 12, 13) else value % 10
    return f"{value}{P_(f'{digit} ({gender})', _ORDINAL_SUFFIXES[digit])}"


def ordinal(num):
    """Return ordinal number string of num, e.g. 1 becomes 1st.
    """
    # modified from https://codereview.stackexchange.com/questions/41298/producing-ordinal-numbers
    n = as_int(num)
    k = abs(n) % 100
    if 11 <= k <= 13:
        suffix = 'th'
    elif k % 10 == 1:
        suffix = 'st'
    elif k % 10 == 2:
        suffix = 'nd'
    elif k % 10 == 3:
        suffix = 'rd'
    else:
        suffix = 'th'
    return str(n) + suffix

