from typing import Any

def colorValidator(value: Any) -> bool:
    """
    Version 3+.

    >>> colorValidator("0,0,0,0")
    True
    >>> colorValidator(".5,.5,.5,.5")
    True
    >>> colorValidator("0.5,0.5,0.5,0.5")
    True
    >>> colorValidator("1,1,1,1")
    True

    >>> colorValidator("2,0,0,0")
    False
    >>> colorValidator("0,2,0,0")
    False
    >>> colorValidator("0,0,2,0")
    False
    >>> colorValidator("0,0,0,2")
    False

    >>> colorValidator("1r,1,1,1")
    False
    >>> colorValidator("1,1g,1,1")
    False
    >>> colorValidator("1,1,1b,1")
    False
    >>> colorValidator("1,1,1,1a")
    False

    >>> colorValidator("1 1 1 1")
    False
    >>> colorValidator("1 1,1,1")
    False
    >>> colorValidator("1,1 1,1")
    False
    >>> colorValidator("1,1,1 1")
    False

    >>> colorValidator("1, 1, 1, 1")
    True
    """
    if not isinstance(value, str):
        return False
    parts = value.split(",")
    if len(parts) != 4:
        return False
    for part in parts:
        part = part.strip()
        converted = False
        number: IntFloat
        try:
            number = int(part)
            converted = True
        except ValueError:
            pass
        if not converted:
            try:
                number = float(part)
                converted = True
            except ValueError:
                pass
        if not converted:
            return False
        if not 0 <= number <= 1:
            return False
    return True

