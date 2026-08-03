from typing import Any

def fontInfoVersion3OpenTypeOS2PanoseValidator(values: Any) -> bool:
    """
    Version 3+.
    """
    if not isinstance(values, (list, tuple)):
        return False
    if len(values) != 10:
        return False
    for value in values:
        if not isinstance(value, int):
            return False
        if value < 0:
            return False
    # XXX further validation?
    return True

