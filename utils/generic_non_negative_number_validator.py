from typing import Any

def genericNonNegativeNumberValidator(value: Any) -> bool:
    """
    Generic. (Added at version 3.)
    """
    if not isinstance(value, numberTypes):
        return False
    if value < 0:
        return False
    return True

